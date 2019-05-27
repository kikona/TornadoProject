import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 模板路径
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

# 静态文件路径
STATIC_PATH = os.path.join(BASE_DIR, 'static')


# 数据库
url = 'mysql+pymysql://root:kyq31415926@localhost:3306/tornadodb'
ENGINE = create_engine(url)

# 指定模型和数据库中表的关联关系的基类，然后让模型基础基类
# 生成的时候，也要绑定一下数据库
BASE_DB = declarative_base(bind=ENGINE)

SESSIONMAKER = sessionmaker(bind=ENGINE)
session = SESSIONMAKER()

