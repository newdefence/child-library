# coding=utf-8
__author__ = 'defence.zhang@gmail.com'
__date__ = "2020/09/14 上午9:38:00"

from datetime import datetime, date
from json import JSONEncoder

from tornado.web import Application, RequestHandler

class JSONEncoder2(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, o)


JSON_ENCODER = JSONEncoder2(ensure_ascii=False)

class BaseHandler(RequestHandler):

    def check_xsrf_cookie(self):
        pass

    def set_etag_header(self):
        pass

    def check_etag_header(self):
        pass

    # def options(self, *args, **kwargs):
    #     self.set_header("Allow", "GET")

    def write(self, chunk):
        if isinstance(chunk, dict):
            chunk = JSON_ENCODER.encode(chunk).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(BaseHandler, self).write(chunk)

