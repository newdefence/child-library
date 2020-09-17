# coding=utf-8
__author__ = 'defence.zhang@gmail.com'
__date__ = "2018/11/20 下午9:38:00"

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os
from datetime import datetime

from tornado.ioloop import IOLoop
from tornado.log import app_log
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler

define("port", default=9999, type=int, help="服务运行端口")
define("debug", default=True, type=bool, help="服务运行模式")
parse_command_line()

try:
    import config
except ImportError:
    print "please create py/config/%s.py and modify it correctly as py/config/simple.py ..." % ('local' if options.debug else 'online')
    exit()

import base

def main():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        cookie_secret=datetime.today().strftime("CHILD_LIBRARY%Y"),
        debug=options.debug,
        autoescape=None
    )
    handlers = [
        # # (r'/wx/cj.html', wx.QrCodeHandler),
        # (r'/qrcode/(\w+)/(\w+)', wx.QrCodeHandler),
        # (r'/wx/post.json', wx.PostAddressHandler),
        # # 后台接口
        # (r'/activity', activity.ActivityHandler),
        # (r'/activity/(\w+)/qrcode', activity.QrCodePageHandler), # 二维码图像列表页面
        # (r'/activity/(\w+)/qrcode/(\w+)', activity.QRCodeHander), # GET 单个二维码图像, id, seq, salt
        (r'/rd/login', base.LoginHandler),
        (r'/rd/books', base.BooksHandler),
    ]
    # if options.debug:
    #     handlers += [
    #         (r'/test.html', TestHandler),
    #     ]


    application = Application(handlers, **settings)
    # Forks one process per CPU.
    application.listen(options.port, xheaders=True) # .start(0)
    # Now, in each child process, create a MotorClient.
    # application.settings['db'] = MotorClient(config.mongodb).cj
    app_log.warning("library server start at port: %s" % options.port)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()

