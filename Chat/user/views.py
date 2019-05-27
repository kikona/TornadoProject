import uuid
from datetime import datetime, timedelta
import tornado.web

from user.forms import RegisterForm, LoginForm
from user.models import create_db, User, UserToken
from utils.settings import session


class InitDbHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        create_db()
        self.write('初始化数据库成功')

class RegisterHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):

        self.render('register.html')

    def post(self, *args, **kwargs):
        # 取值
        # account = self.get_argument('account')
        # password = self.get_argument('password')
        # password2 = self.get_argument('password2')

        # 自定义表单做校验，判断注册的账号和密码等信息
        form = RegisterForm()
        result, errors = form.check_valid(self)
        if result:
            # 校验字段成功，校验密码是否一致，保存信息
            pwd1 = self.get_argument('password')
            pwd2 = self.get_argument('password2')
            if pwd1 != pwd2:
                errors['password'] = '密码和确认密码不一致'
            # 保存到数据库
            user = User()
            user.account = self.get_argument('account')
            user.password = self.get_argument('password')
            user.save()
            # 重定向到登录地址
            self.redirect('/login/')

        # 校验失败
        self.render('register.html', errors=errors)


class LoginHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):

        self.render('login.html')

    def post(self, *args, **kwargs):
        # 使用表单校验
        form = LoginForm()
        result, errors = form.check_valid(self)
        if result:
            # 登录操作
            account = self.get_argument('account')
            password = self.get_argument('password')
            user = session.query(User).filter_by(account=account, password=password).first()

            if not user:
                errors['account'] = '账号或密码错误'
                self.render('login.html', errors=errors)
            # 账号和密码正确，能找到用户信息

            token = uuid.uuid4().hex
            self.set_cookie('token', token, expires_days=1)

            # 定义后端存储token和user的表，将token和user保存起来
            # 单点登录
            # 如果已经有该用户，则更新，没有就创建, 这样的话，一个用户就只有一个信息
            old_user_token = session.query(UserToken).filter(UserToken.user_id == user.id).first()
            if old_user_token:
                old_user_token.token = token
                old_user_token.out_time = datetime.now() + timedelta(days=1)
                session.add(old_user_token)  # 准备向数据库插入数据
                session.commit()  # 提交到数据
            else:
                user_token = UserToken()
                user_token.token = token #tornado
                user_token.user_id = user.id
                user_token.out_time = datetime.now() + timedelta(days=1)

                session.add(user_token)  # 准备向数据库插入数据
                session.commit()  # 提交到数据

            self.redirect('/home/')
            return  # 避免重定向之后，又返回模板

        # 参数校验失败
        self.render('login.html', errors=errors)