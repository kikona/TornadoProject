'''
同步
'''
import tornado.web
import tornado.ioloop
import tornado.httpclient

class SearchHandler(tornado.web.RequestHandler):


    def get(self, *args, **kwargs):
        # 获取百度搜索某个资源的源码
        # 地址：https://www.baidu.com/s?wd=ab
        wd = self.get_argument('wd')
        # 获取 http 客户端
        client = tornado.httpclient.HTTPClient()
        # fetch(): 获取某个地址的响应结果
        print('同步操作开始')
        response = client.fetch('https://www.baidu.com/s?wd={}'.format(wd))
        print(response)
        self.write('获取百度搜索某个资源的源码')



def make_app():
    return tornado.web.Application(handlers=[
        ('/search/', SearchHandler)
    ])

if __name__ == '__main__':

    app = make_app()

    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()