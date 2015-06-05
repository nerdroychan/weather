import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.httpclient
import tornado.gen
import json

from tornado.options import define, options
define('port', default = 8967, help = "run on the given port", type = int)

'''class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, 'http://www.weibo.cn')
        self.write('hello, world')
        self.finish()'''

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            ipAddr = self.request.headers['X-Forwarded-For']
        except KeyError:
            ipAddr = self.request.remote_ip

        client = tornado.httpclient.AsyncHTTPClient()
        geoIpResponse = yield tornado.gen.Task(client.fetch, 'https://freegeoip.net/json/' + ipAddr)
        geoInfo = json.loads(str(geoIpResponse.body))
        latitude, longitude = geoInfo['latitude'], geoInfo['longitude']
        self.write(latitude + longitude)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r'^/$', IndexHandler),    
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()