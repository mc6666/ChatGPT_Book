from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import os, base64, hashlib, hmac, openai

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

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    model = 'text-davinci-003'
    max_tokens = 200
    temperature = 0
    response = openai.Completion.create(
        model=model,
        prompt=text,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # 顯示回答
    # profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=response.choices[0].text),
        ]
    )

if __name__ == "__main__":
    app.run(debug=True)
