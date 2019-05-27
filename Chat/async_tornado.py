'''
异步（耗时）
'''
import tornado.web
import tornado.ioloop
import tornado.httpclient


class SearchHandler(tornado.web.RequestHandler):
    # asynchronous装饰器，表示io不主动关闭，拿到响应之后才关闭
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        # 异步操作
        wd = self.get_argument('wd')
        print('异步操作开始')
        client = tornado.httpclient.AsyncHTTPClient()
        # 如果阻塞，不会等待响应，当有响应结果时就自动执行回调的函数
        client.fetch('https://www.baidu.com/s?wd={}'.format(wd),
                     callback=self.on_response)

    def on_response(self, response):
        print(response)       # 响应结果
        print('异步操作结束')
        # 手动关闭io
        self.finish()


def make_app():
    return tornado.web.Application(handlers=[
        ('/search/', SearchHandler)
    ])


if __name__ == '__main__':

    app = make_app()

    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()