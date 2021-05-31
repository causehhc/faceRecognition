from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

# 生成一个SQLORM基类，创建表必须继承他
Base = declarative_base()


class Person_info(Base):
    __tablename__ = 'person_info'
    PID = Column(Integer(), primary_key=True)
    PName = Column(String(190))
    PSex = Column(String(190))
    PImgID = Column(Integer())
    PPhone = Column(String(190))


class Check_log(Base):
    __tablename__ = 'check_log'
    CID = Column(Integer(), primary_key=True)
    CTime = Column(DateTime())
