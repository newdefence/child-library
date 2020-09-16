# coding=utf-8
__author__ = 'defence.zhang@gmail.com'
__date__ = "2020/09/14 上午9:38:00"

from datetime import datetime, date
from json import JSONEncoder

from tornado_mysql.pools import Pool
from tornado_mysql.cursors import DictCursor

from tornado.web import Application, RequestHandler

class JSONEncoder2(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, o)


COOKIE_KEY = 'uid'
JSON_ENCODER = JSONEncoder2(ensure_ascii=False)

Db_Pool = Pool(dict(
        host="localhost", user="web", passwd="qaz123", database="child_library", charset="utf8mb4",
        cursorclass=DictCursor, connect_timeout=1000
    ), max_open_connections=30)

class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_id, user = self.get_secure_cookie(COOKIE_KEY), None
        if not user_id: return None
        return { 'name': '测试账户', 'id': user_id }
    # def check_xsrf_cookie(self):
    #     pass

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

class LoginHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        if self.application.settings['debug']:
            self.set_secure_cookie(COOKIE_KEY, 'TEST_USER')
            self.finish({'success': True, 'msg': '登录成功'})
        else:
            raise HTTPError(404)

    def post(self):
        user = loads(self.request.body)
        self.set_secure_cookie(COOKIE_KEY, user['name'])
        self.finish({'success': True, 'msg': '登录成功'})

    def put(self):
        self.clear_cookie(COOKIE_KEY)
        self.finish({'success': True, 'msg': '退出成功'})

class BooksHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self, *args, **kwargs):
        where, params = [], []
        keyword, age, topic, lang = [self.get_query_argument(k, None) for k in ('keyword', 'age', 'topic', 'lang')]
        if keyword:
            where.append('(`isbn`=%s OR `code`=%s OR name LIKE %s)')
            params.append(keyword, keyword, '%' + keyword + '%')
        if age:
            where.append('`forAge`=%s')
            params.append(age)
        if topic:
            where.append('`topic`=%s')
            params.append(topic)
        if lang:
            where.append('`lang`=%s')
            params.append(lang)
        wheres = ' WHERE %s' % ' AND '.join(where) if where else ''
        cursor = yield Db_Pool.execute('SELECT COUNT(`id`) AS total FROM `books` %s;' % wheres, params)
        total = cursor.fetchone()['total']
        cursor = yield Db_Pool.execute('SELECT * FROM `books` %s ORDER BY created DESC;' % wheres, params)
        books = cursor.fetchall()
        self.finish({
            'total': total,
            'data': books
        })

class BookHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self, *args, **kwargs):
        pass

    @coroutine
    @authenticated
    def post(self, *args, **kwargs):
        pass

    @coroutine
    @authenticated
    def put(self, *args, **kwargs):
        pass

    @coroutine
    @authenticated
    def delete(self, *args, **kwargs):
        pass


