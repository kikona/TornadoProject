
import tornado.web
import tornado.ioloop
from tornado.options import options, define, parse_command_line
from tornado_jinja2 import Jinja2Loader

from chat.views import HomeHandler,ManyChatHandler,ChatHandler
from utils.settings import TEMPLATE_PATH, STATIC_PATH
from user.views import RegisterHandler, InitDbHandler,LoginHandler

jinja2loader = Jinja2Loader('templates')

define('port', default=8000, type=int)


def make_app():
    return tornado.web.Application(handlers=[
        ('/register/', RegisterHandler),
        ('/init_db/', InitDbHandler),
        ('/login/', LoginHandler),
        ('/home/', HomeHandler),
        ('/many_chat/', ManyChatHandler),
        ('/chat/', ChatHandler),

    ],
    template_path=TEMPLATE_PATH,
    static_path=STATIC_PATH,
    template_loader=jinja2loader,
    )

if __name__ == '__main__':
    parse_command_line()

    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()