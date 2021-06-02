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
        now = datetime.datetime.now()
        item_list = self._db.session.query(Check_log).all()
        item = item_list[0]
        print((now-item.CTime).days)

    def clear(self):
        self._db.session.query(Person_info).delete()
        self._db.session.commit()

    def get_info_all(self):
        item_list1 = self._db.session.query(Person_info).all()
        item_list2 = self._db.session.query(Check_log).all()
        res1 = []
        res2 = []
        temp_dict = {}
        for item in item_list1:
            temp_dict[item.PID] = item
            res1.append([item.PID, item.PName, item.PSex, item.PImgID, item.PPhone])
        for item in item_list2:
            temp = temp_dict[item.PID]
            res2.append([temp.PName, temp.PSex, temp.PImgID, temp.PPhone, str(item.CTime)])
        return res1, res2

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

    def get_log(self, category, text):
        if text != '':
            if category == 'PID':
                item_list = self._db.session.query(Person_info).filter_by(PID=text).all()
            elif category == 'PName':
                item_list = self._db.session.query(Person_info).filter_by(PName=text).all()
            elif category == 'PSex':
                item_list = self._db.session.query(Person_info).filter_by(PSex=text).all()
            elif category == 'PImgID':
                item_list = self._db.session.query(Person_info).filter_by(PImgID=text).all()
            elif category == 'PPhone':
                item_list = self._db.session.query(Person_info).filter_by(PPhone=text).all()
            else:
                item_list = None
        else:
            item_list = self._db.session.query(Person_info).all()

        res = []
        for item in item_list:
            item_log_list = self._db.session.query(Check_log).filter_by(PID=item.PID).all()
            for item_log in item_log_list:
                res.append([item.PName, item.PSex, item.PImgID, item.PPhone, str(item_log.CTime)])
        return res

    def get_log_time(self, category):
        res = []
        now = datetime.datetime.now()
        item_list = self._db.session.query(Check_log).all()
        for item in item_list:
            if category == 'All':
                pass
            elif category == 'Day':
                if (now - item.CTime).days >= 1:
                    continue
            elif category == 'Week':
                if (now - item.CTime).days >= 7:
                    continue
            elif category == 'Month':
                if (now - item.CTime).days >= 30:
                    continue
            else:
                pass

            item_info = self._db.session.query(Person_info).filter_by(PID=item.PID).first()
            res.append([item_info.PName, item_info.PSex, item_info.PImgID, item_info.PPhone, str(item.CTime)])
        return res

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
    h = MySqlHelper()
    h.get_test()
    # h.clear()
    # h.add_info(['1', '1', '1', '1'])
    # theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    # h.create_log(1, theTime)

