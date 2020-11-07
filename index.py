import tornado.ioloop
import tornado.web
import sys
import os

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(f"Served from {os.getpid()}")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/basic", basicRequestHandler)
    ])

    port = 8882
    if (sys.argv.__len__() > 1):
        port = sys.argv[1]

    app.listen(port)
    print(f"Application is ready and listening on port {port}")
    tornado.ioloop.IOLoop.current().start()