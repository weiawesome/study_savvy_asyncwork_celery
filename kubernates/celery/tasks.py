import random
import string
from email.message import EmailMessage
from celery import Celery
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from mail_content import getMailContent
from redis import Redis, ConnectionPool
from models.File import File
from utils import decrypt
from ASR.ASR_Module import transcribe
from NLP.RevChat import revChat, revChat_test
from NLP.open_AI_chat import openaiChat, openaiChat_test
from OCR.Craft_TrOCR import image_to_texts
from celery import Task
import smtplib
import env

dsn="mysql+pymysql://{}:{}@{}/{}".format(env.MYSQL_USER,env.MYSQL_PASSWORD,env.MYSQL_ADDRESS,env.MYSQL_DB)

engine = create_engine(dsn)
metadata = MetaData()
Session = scoped_session(sessionmaker(bind=engine))

REDIS_PASSWORD = env.REDIS_PASSWORD
REDIS_ADDRESS  =  env.REDIS_ADDRESS
REDIS_HOST  =  env.REDIS_HOST
REDIS_PORT  =  env.REDIS_PORT
REDIS_DB  =  env.REDIS_DB
MAIL_USER=env.MAIL_USER
MAIL_PASSWORD=env.MAIL_PASSWORD

celery_app = Celery(
    "celery",
    broker="redis://:{}@{}/{}".format(REDIS_PASSWORD,REDIS_ADDRESS,REDIS_DB),
    summarize_expires=3600,
)

pool = ConnectionPool(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB),password=REDIS_PASSWORD)

class DatabaseTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        session = Session()
        try:
            task_summarize = session.get(File, kwargs["id"])
            if task_summarize is not None:
                task_summarize.status = "SUCCESS"
                task_summarize.result = retval
                session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            Session.close()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        session = Session()
        try:
            task_summarize = session.get(File, kwargs["id"])
            if task_summarize is not None:
                task_summarize.status = "FAILURE"
                session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            Session.close()


@celery_app.task(bind=True, base=DatabaseTask)
def ASR_predict(self,id,file, prompt,api_key,access_token,key_api_key,key_access_token):
    api_key=decrypt(api_key,key_api_key)
    access_token=decrypt(access_token,key_access_token)
    content = transcribe(file)
    response={"prompt":prompt,"content":content,"summarize":"","details":[]}
    if revChat_test(access_token=access_token):
        details, summarize = revChat(access_token=access_token, mode="ASR", prompt=prompt, text=content)
        response["summarize"]=summarize
        response["details"]=details
    elif openaiChat_test(api_key-api_key):
        details, summarize = openaiChat(api_key=api_key, mode="ASR", prompt=prompt, text=content)
        response["summarize"]=summarize
        response["details"]=details
    return response


@celery_app.task(bind=True, base=DatabaseTask)
def OCR_predict(self,id,file, prompt,api_key,access_token,key_api_key,key_access_token):
    api_key=decrypt(api_key,key_api_key)
    access_token=decrypt(access_token,key_access_token)
    content = image_to_texts(file)
    response = {"prompt": prompt, "content": content, "summarize": "", "details": []}
    if revChat_test(access_token=access_token):
        details, summarize = revChat(access_token=access_token, mode="OCR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    elif openaiChat_test(api_key=api_key):
        details, summarize = openaiChat(api_key=api_key, mode="OCR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    return response

@celery_app.task(bind=True, base=DatabaseTask)
def OCR_predict_Text(self,id,content, prompt,api_key,access_token,key_api_key,key_access_token):
    api_key=decrypt(api_key,key_api_key)
    access_token=decrypt(access_token,key_access_token)
    response = {"prompt": prompt, "content": content, "summarize": "", "details": []}
    if revChat_test(access_token=access_token):
        details, summarize = revChat(access_token=access_token, mode="OCR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    elif openaiChat_test(api_key=api_key):
        details, summarize = openaiChat(api_key=api_key, mode="OCR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    return response

@celery_app.task(bind=True, base=DatabaseTask)
def NLP_edit_OCR(self,id,content, prompt,api_key,access_token,key_api_key,key_access_token):
    api_key=decrypt(api_key,key_api_key)
    access_token=decrypt(access_token,key_access_token)
    response = {"prompt": prompt, "content": content, "summarize": "", "details": []}
    if revChat_test(access_token=access_token):
        details, summarize = revChat(access_token=access_token, mode="OCR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    elif openaiChat_test(api_key=api_key):
        details, summarize = openaiChat(api_key=api_key, mode="OCR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    return response



@celery_app.task(bind=True, base=DatabaseTask)
def NLP_edit_ASR(self,id,content, prompt,api_key,access_token,key_api_key,key_access_token):
    api_key=decrypt(api_key,key_api_key)
    access_token=decrypt(access_token,key_access_token)
    response = {"prompt": prompt, "content": content, "summarize": "", "details": []}
    if revChat_test(access_token=access_token):
        details, summarize = revChat(access_token=access_token, mode="ASR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    elif openaiChat_test(api_key=api_key):
        details, summarize = openaiChat(api_key=api_key, mode="ASR", prompt=prompt, text=content)
        response["summarize"] = summarize
        response["details"] = details
    return response


@celery_app.task(bind=True)
def Mail_sent(self,mail):
    redis_client = Redis(connection_pool=pool)
    code = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    email_body = getMailContent(code=code)
    with smtplib.SMTP(host="smtp.gmail.com") as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(MAIL_USER,MAIL_PASSWORD)
            content = EmailMessage()
            sender_name="Study Savvy"
            content["From"] = f"{sender_name} <{MAIL_USER}>"
            content["To"] = mail
            content["Subject"] = "StudySavvy 信箱認證 (Verification of email for StudySavvy)"
            content.set_content(email_body,"html")
            smtp.send_message(content)
        except Exception as e:
            return
        redis_client.set(mail, code)
        redis_client.expire(mail, 600)
    return