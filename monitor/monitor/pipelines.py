# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import io
from scrapy import Item
from scrapy.conf import settings
import pymongo
import smtplib
import os
from email.mime.text import MIMEText

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

content = ""
flag = False
mail_host = "smtp.163.com"
mail_user = os.environ["MAIL_USER"]
sender = os.environ["SENDER"]
receivers = os.environ["RECEIVER"]
mail_pass = os.environ["MAIL_PASS"]

def send(content):
    message = MIMEText(content, "plain", "utf-8")
    message["Subject"] = 'Update'
    message["From"] = sender
    message["To"] = receivers[0]

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()

    except smtplib.SMTPException as e:
        print("Error:", e)

class MonitorPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbName = settings["MONGODB_DBNAME"]
        self.client = pymongo.MongoClient(host = host, port = port)
        tdb = self.client[dbName]
        self.post = tdb[settings["MONGODB_DOCNAME"]]
        self.query = tdb[settings["MONGODB_DOCNAME"]]

    def process_item(self, item, spider):
        news = dict(item)
        res = self.post.find_one({'news_url' : news["news_url"]})
        global content
        global flag

        if not res:
            flag = True
            self.post.insert_one(news).inserted_id
            content ="[" +getSchool(news["news_url"]) + "]"+content + news["news_url"] + " " + news["news_title"][0]
            content = content + "\n"
#            print(content)

        return item

    def close_spider(self, spider):
        global flag

        if flag:
            global content
            send(content)
        self.client.close()

def getSchool(url):
    return url.split(".")[1]
