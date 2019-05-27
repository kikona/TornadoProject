from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship

from utils.settings import BASE_DB, session


def create_db():
    # 迁移模型，映射成表
    BASE_DB.metadata.create_all()

class User(BASE_DB):
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(10), unique=True, nullable=False)
    password = Column(String(10),nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    token = relationship('UserToken', backref='user')

    __tablename__ = 'user'

    def save(self):
        session.add(self)  # 准备向数据库插入数据
        session.commit()    # 提交到数据


class UserToken(BASE_DB):
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(200), unique=True, nullable=False)
    out_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    __tablename__ = 'user_token'