'''
异步（耗时）
'''
import tornado.web
import tornado.ioloop
import tornado.httpclient


class SearchHandler(tornado.web.RequestHandler):

    # 将异步回调程序 写成类似于同步的代码，但有异步效果
    # @tornado.web.gen.coroutine      # 协程装饰器
    # def get(self, *args, **kwargs):
    #     wd = self.get_argument('wd')
    #     print('异步操作开始')
    #     client = tornado.httpclient.AsyncHTTPClient()
    #     print('协程开始')
    #     # 如果阻塞，不会等待响应，当有响应结果时就自动执行回调的函数
    #     response = yield client.fetch('https://www.baidu.com/s?wd={}'.format(wd))
    #     print(response)


# async 和 await 是python自带的，加上就可以让程序变成 协程
    async def get(self, *args, **kwargs):
        wd = self.get_argument('wd')
        client = tornado.httpclient.AsyncHTTPClient()
        print('协程开始')
        # 如果阻塞，不会等待响应，当有响应结果时就自动执行回调的函数
        response = await client.fetch('https://www.baidu.com/s?wd={}'.format(wd))
        print(response)


def make_app():
    return tornado.web.Application(handlers=[
        ('/search/', SearchHandler)
    ])


if __name__ == '__main__':

    app = make_app()

    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()