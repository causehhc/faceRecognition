import asyncio
import datetime
import re
import uuid
import aiohttp
import feedparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from backend.models import *
import time
from datetime import datetime


class MySession:
    def __init__(self, sess):
        self.session = sess


class MySqlHelper:
    def __init__(self):
        user = 'root'
        passwd = 'password'
        host = 'localhost'
        name = 'comprehensive_design_3'
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8mb4".format(user, passwd, host, name)
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        self._db = MySession(session)

    def get_test(self):
        temp = self._db.session.query(Person_info).all()
        for item in temp:
            print(item.PID, item.PName)


if __name__ == '__main__':
    h = MySqlHelper()
    h.get_test()
