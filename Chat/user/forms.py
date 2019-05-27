import re


class BaseForm():

    def check_valid(self, request):
        # 做校验，将初始化的字段和请求传入的字段进行匹配
        # self.__dict__ 拿到的是对象初始化的字段和值
        flag = True
        # 用于存储错误信息
        errors = {}
        for key, value in self.__dict__.items():
            post_value = request.get_argument(key)
            # 进行正则匹配
            if not re.match(value, post_value):
                flag = False
                errors[key] = '%s字段校验不成功' % key

        return flag, errors


class RegisterForm(BaseForm):

    # 注册表单，用于校验注册信息
    def __init__(self):
        # 账号只能为5-10位的字母
        self.account = '[a-zA-Z]{5,10}'
        # 密码
        self.password = '[0-9]{5,10}'
        # 确认密码
        self.password2 = '[0-9]{5,10}'




class LoginForm(BaseForm):

    # 登录表单，用于校验登录信息
    def __init__(self):
        # 账号只能为5-10位的字母
        self.account = '[a-zA-Z]{5,10}'
        # 密码
        self.password = '[0-9]{5,10}'
