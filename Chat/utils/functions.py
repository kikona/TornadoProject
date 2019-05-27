# 装饰器
# 条件：1.外层函数内嵌内层函数
#       2.外层函数返回内层函数
#       3.内层函数调用外层函数的参数
from datetime import datetime
from functools import wraps

from user.models import UserToken, User
from utils.settings import session


def login_required(fn):

    @wraps(fn)  # 避免反向解析出问题，flask里必须加
    def check(self,*args, **kwargs):
        # 如果登录校验成功，返回fn()
        token = self.get_cookie('token')
        # 用户和token为一对一的关系
        user_token = session.query(UserToken).filter(UserToken.token == token).first()
        if user_token:
            # 能通过token查询到UserToken表中的数据
            # 判断token是否过期
            if user_token.out_time > datetime.now():
                # requset中自定义一个user属性，并赋值为当前登录系统的用户对象
                user = session.query(User).get(user_token.user_id)
                self.request.user = user
                return fn(self, *args, **kwargs)
        # 重定向到登录地址
        self.redirect('/login/')


    return check