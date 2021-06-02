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
import datetime


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

    def clear(self):
        self._db.session.query(Person_info).delete()
        self._db.session.commit()

    def add_info(self, info_list):
        item = Person_info()
        item.PID = info_list[2]
        item.PName = info_list[0]
        item.PSex = info_list[1]
        item.PImgID = info_list[2]
        item.PPhone = info_list[3]
        self._db.session.add(item)
        self._db.session.commit()

    def del_info(self, info_list):
        item = self._db.session.query(Person_info).filter_by(PID=info_list[2]).first()
        if item is not None:
            self._db.session.delete(item)
            self._db.session.commit()

    def get_info(self, info_pid):
        item = self._db.session.query(Person_info).filter_by(PID=info_pid).first()
        if item is not None:
            return [item.PName, item.PSex, item.PImgID, item.PPhone]
        return None

    def change_info(self, info_list):
        item = self._db.session.query(Person_info).filter_by(PID=info_list[2]).first()
        item.PID = info_list[2]
        item.PName = info_list[0]
        item.PSex = info_list[1]
        item.PImgID = info_list[2]
        item.PPhone = info_list[3]
        self._db.session.commit()

    def update_info(self, info_list, face_class):
        if info_list[2] != face_class:
            item = self._db.session.query(Person_info).filter_by(PID=face_class).first()
            item.PID = info_list[2]
            item.PName = info_list[0]
            item.PSex = info_list[1]
            item.PImgID = info_list[2]
            item.PPhone = info_list[3]
        else:
            item = Person_info()
            item.PID = info_list[2]
            item.PName = info_list[0]
            item.PSex = info_list[1]
            item.PImgID = info_list[2]
            item.PPhone = info_list[3]
            self._db.session.add(item)
        self._db.session.commit()

    def create_log(self, face_class, t):
        item = Check_log()
        item.CID = uuid.uuid1()
        item.PID = face_class
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
        item.CTime = t.strftime(ISOTIMEFORMAT)
        self._db.session.add(item)
        self._db.session.commit()


if __name__ == '__main__':
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
    h = MySqlHelper()
    # h.clear()
    # h.add_info(['1', '1', '1', '1'])
    # theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    # h.create_log(1, theTime)
    t1 = datetime.datetime.now()
    time.sleep(3)
    t2 = datetime.datetime.now()
    print((t2-t1).seconds)
