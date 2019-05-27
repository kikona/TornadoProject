
import tornado.web
import tornado.websocket    # 长连接的包

from utils.functions import login_required


class HomeHandler(tornado.web.RequestHandler):

    @login_required
    def get(self, *args, **kwargs):
        self.render('home.html')



class ManyChatHandler(tornado.web.RequestHandler):

    @login_required
    def get(self, *args, **kwargs):

        self.render('chat.html')


class ChatHandler(tornado.websocket.WebSocketHandler):
    # 将建立长连接的用户保存起来
    many_user_online = []

    @login_required
    # open() 是建立socket连接时，默认调用的方法
    def open(self, *args, **kwargs):
        self.many_user_online.append(self)
        # 将进入聊天室的欢迎信息广播给所有的在线用户
        for chat_user in self.many_user_online:
            user = self.request.user
            chat_user.write_message('系统提示:{}已进入聊天室'.format(user.account))

    @login_required
    # message 为前端发送消息，需要将message信息广播给其他用户
    def on_message(self, message):
        for chat_user in self.many_user_online:
            if chat_user != self:
                user = self.request.user
                chat_user.write_message('{}说：{}'.format(user.account,message))


    @login_required
    # 关闭连接时，默认调用的方法，只要退出聊天界面，就算关闭连接
    def on_close(self):
        self.many_user_online.remove(self)
        # 将退出聊天室的提示信息广播给还在线的所有用户
        for chat_user in self.many_user_online:
            user = self.request.user
            chat_user.write_message('系统提示:{}已退出聊天室'.format(user.account))
