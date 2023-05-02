# 載入套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import os, base64, hashlib, hmac, tempfile, openai
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db_schema import *
from linebot.models import ImageMessage, VideoMessage, AudioMessage, ImageSendMessage

# 指定 Channel secret、Channel access token
CHANNEL_ACCESS_TOKEN=os.environ.get('CHANNEL_ACCESS_TOKEN', '')
CHANNEL_SECRET=os.environ.get('CHANNEL_SECRET', '')

# 建立 Flask 物件 
app = Flask(__name__)

# 設定工作日誌檔名及訊息欄位
logging.basicConfig(filename='record.log', encoding='utf-8', 
    level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# 建立 LineBot物件
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# 建立 Webhook 處理函數
# parser = WebhookParser(CHANNEL_SECRET)
handler = WebhookHandler(CHANNEL_SECRET)

# 建立訊息處理函數
@app.route("/callback", methods=['POST'])
def callback():
    # 取得表頭的Line簽名(Signature)
    signature = request.headers['X-Line-Signature']

    # 取得接收訊息
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # 檢驗訊息是否來自Line平台
    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'),
            body.encode('utf-8'), hashlib.sha256).digest()
    signature_hash = base64.b64encode(hash)

    if signature != signature_hash.decode("utf-8"):
        raise Exception(InvalidSignatureError)
        abort(400)
        
    # 解析 body 訊息
    try:
        # events = parser.parse(body, signature)
        handler.handle(body, signature)
    except LineBotApiError as e:
        app.logger.error(f"LINE Messaging API error: {e.message}\n")
        for m in e.error.details:
            app.logger.error(f"  {m.property}, {m.message}")
        abort(500)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        app.logger.error(f"LINE Messaging API error: {str(e)}\n")
        abort(500)

    return 'OK'

# 新增或取得使用者資訊
def create_user(engine, user_id):
    session = Session(engine)
    stmt = select(User).where(User.line_id == user_id)
    user1 = session.scalars(stmt).one_or_none()
    if user1 is not None:
        return user1
    profile = line_bot_api.get_profile(user_id)
    user1 = User(
        line_id=user_id,
        display_name=profile.display_name,
        topic="聊天",
    )
    session.add_all([user1])
    session.commit()
    return user1
    
# 更新使用者資訊
def update_user_preference(engine, user, topic):
    session = Session(engine)
    session.add(user)
    user.topic = topic
    session.commit()

# 取得模型定義
def get_model(engine, topic):
    session = Session(engine)
    stmt = select(Model).where(Model.topic == topic)
    model = session.scalars(stmt).one_or_none()
    return model
    
# 呼叫 ChatGPT API
def call_ChatGPT_api(model, text):
    if model.api_function == "Image":
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    else:
        messages=[
            {"role": "system", "content": model.system_prompt},
            {"role": "user", "content": text}
        ]        
        response = openai.ChatCompletion.create(
            model=model.model_id,
            messages=messages,
            # prompt=model.system_prompt + '\n' + text,
            temperature=model.temperature,
            max_tokens=model.max_tokens,
        )
        return response.choices[0].message.content
    

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    
    # 資料庫連線
    engine = create_engine("sqlite:///data/line_db.db", echo=True)
    Base.metadata.create_all(engine)

    # 新增或取得使用者資訊
    user = create_user(engine, event.source.user_id)
    if text.startswith('T:'):
        topic = text[2:].strip()
        # 取得模型定義
        model = get_model(engine, topic)
        if model is None:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='無此功能 !!'),
                ]
            )
            return 

        # 更新使用者資訊
        update_user_preference(engine, user, topic)
        
        # 回應【已設定】
        line_bot_api.reply_message(
            event.reply_token, [
                    TextSendMessage(text='已設定 !!'),
            ]
        )
    else:
        # 取得模型定義
        model = get_model(engine, user.topic)

        # 呼叫 ChatGPT API
        response = call_ChatGPT_api(model, text)

        # 回答
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=response),
            ]
        )


# 圖像(ImageMessage)、影片(VideoMessage)、語音(AudioMessage)訊息接收與處理
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    # 判斷訊息類別
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    # 取得訊息內容
    if isinstance(event.message, AudioMessage):
        message_content = line_bot_api.get_message_content(event.message.id)
        # 存檔
        sub_path = os.path.join('static', 'tmp')
        static_tmp_path = os.path.join(os.path.dirname(__file__), sub_path)
        if not os.path.exists(static_tmp_path):
            os.makedirs(static_tmp_path,  exist_ok = True)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext+'-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        # 搬移至程式目錄下的 static\tmp 子目錄
        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
    
        audio= open(dist_path, "rb")
        response = openai.Audio.translate("whisper-1", audio)

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=response.text),
            ]
        )

if __name__ == "__main__":
    app.run(debug=True)
