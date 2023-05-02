from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from db_schema import *

engine = create_engine("sqlite:///data/line_db.db", echo=True)
Base.metadata.create_all(engine)

stmt = select(User).where(User.display_name == "user1")
session = Session(engine)
user1 = session.scalars(stmt).one_or_none()
if user1 is not None:
    exit()
with Session(engine) as session:
    user1 = User(
        line_id="Ude0000f85858cf19238f2c5a079c9e11",
        display_name="user1",
        topic="翻譯",
    )
    user2 = User(
        line_id="Ude0001f85858cf19238f2c5a079c9e22",
        display_name="user2",
        topic="問答",
    )
    models = []
    models.append(Model(
        topic="翻譯",
        model_id="gpt-3.5-turbo",
        api_function="ChatCompletion",
        system_prompt="你是翻譯專家",
        temperature=0.0,
        max_tokens=200,
    ))
    models.append(Model(
        topic="問答",
        model_id="gpt-3.5-turbo",
        api_function="ChatCompletion",
        system_prompt="你是Q&A專家",
        temperature=0.0,
        max_tokens=200,
    ))
    models.append(Model(
        topic="聊天",
        model_id="gpt-3.5-turbo",
        api_function="ChatCompletion",
        system_prompt="你具有創意,友善,會協助他人",
        temperature=0.8,
        max_tokens=200,
    ))
    models.append(Model(
        topic="程式生成",
        model_id="gpt-3.5-turbo", #code-davinci-002",
        api_function="ChatCompletion", # Completion
        system_prompt="你是python專家",
        temperature=0.0,
        max_tokens=200,
    ))
    models.append(Model(
        topic="語音辨識",
        model_id="whisper-1",
        api_function="Audio", 
        system_prompt="你是語音辨識專家",
        temperature=0.0,
        max_tokens=200,
    ))
    models.append(Model(
        topic="圖像生成",
        model_id="",
        api_function="Image", 
        system_prompt="你是圖像生成專家",
        temperature=0.0,
        max_tokens=200,
    ))
    session.add_all([user1, user2])
    session.add_all(models)
    session.commit()
