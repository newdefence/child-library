# coding=utf-8
__author__ = 'defence.zhang@gmail.com'
__date__ = "2020/09/14 上午9:38:00"

from datetime import datetime, date
import functools
import json
import os
import time

from tornado_mysql.pools import Pool
from tornado_mysql.cursors import DictCursor

# from tornado.escape import json_decode
from tornado.gen import coroutine
from tornado.web import HTTPError, RequestHandler

class JSONEncoder2(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)

def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.set_status(403)
            self.finish({ 'success': False, 'message': '请登录' })
        return method(self, *args, **kwargs)
    return wrapper


COOKIE_KEY = 'uid'
JSON_ENCODER = JSONEncoder2(ensure_ascii=False)

Db_Pool = Pool(dict(
        host="localhost", user="web", password="qaz123", database="child_library", charset="utf8mb4",
        cursorclass=DictCursor, connect_timeout=1000
    ), max_open_connections=30)
# 费了4个小时的时间，排除类库的一个BUG，真不值得
# TODO: deprecate server_language and server_charset.
# mysqlclient-python doesn't provide it.
# self.server_charset = charset_by_id(lang).name

class BaseHandler(RequestHandler):
    requestJSON = None
    keyword = None
    start = 0
    size = 0

    def prepare(self):
        if self.request.headers.get("Content-Type", "").lower().find("application/json") == 0 and self.request.body:
            self.requestJSON = json.loads(self.request.body)
        start, size, self.keyword = [self.get_query_argument(key, None) for key in ("start", "size", "keyword")]
        if start and start.isdigit(): self.start = int(start)
        if size and size.isdigit(): self.size = int(size)

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
        user = json.loads(self.request.body)
        self.set_secure_cookie(COOKIE_KEY, user['phone'])
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
            params += [keyword, keyword, '%' + keyword + '%']
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
        self.finish({ 'success': True, 'total': total, 'data': books })

UPLOAD_IMAGE_SUFFIX = {".jpg", ".png", ".jpeg", ".gif", ".bmp", ".webp"}
UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "../public/img/books/%s")
class BookPhotoHandler(BaseHandler):
    def post(self, *args, **kwargs):
        imgName = None
        imgFile = self.request.files['file'][0]
        suffix = os.path.splitext(imgFile["filename"])[1]
        if not suffix:
            suffix = '.jpg'
        bookIdString = self.get_body_argument('bookId', None)
        if not bookIdString:
            bookIdString = 'ts-%s' %time.time()
        if suffix in UPLOAD_IMAGE_SUFFIX:
            imgName = bookIdString + suffix
            imgPath = UPLOAD_IMAGE_PATH % imgName
            # 写文件的各种坑，有的时候写不上文件
            # http://www.oschina.net/translate/reliable-file-updates-with-python
            # http://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/
            with open(imgPath, "wb") as f:
                f.write(imgFile["body"])
                f.flush()
                if hasattr(os, "fdatasync"): os.fdatasync(f.fileno())
                else: os.fsync(f.fileno())  # windows, mac os
        self.finish({ 'success': True, 'url': '/img/books/%s' % imgName })

class BookHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self, *args, **kwargs):
        bookId = self.get_query_argument('id')
        cursor = yield Db_Pool.execute('SELECT * FROM `books` WHERE `id`=%s;', (bookId, ))
        book = cursor.fetchone()
        self.finish({ 'success': True, 'data': book })

    @coroutine
    @authenticated
    def post(self, *args, **kwargs):
        book = self.requestJSON
        cursor = yield Db_Pool.execute('''INSERT INTO `books`
            (isbn,`code`, `name`, price, `status`, created, author, pubDate, photo, intro, remark, lang, tags, forAge)
            VALUE(%s, %s, %s, %s, '在馆', NOW(), %s, %s, %s, %s, %s, %s, %s, %s);''', 
            (book['isbn'], book['code'], book['name'], book['price'], book['author'], book['pubDate'],
            book['photo'], book['intro'], book['remark'], book['lang'], book['tags'], book['forAge']))
        self.finish({ 'success': True, 'id': cursor.lastrowid, 'message': '添加图书成功' })

    @coroutine
    @authenticated
    def put(self, *args, **kwargs):
        bookId, book = self.get_query_argument('id'), self.requestJSON
        cursor = yield Db_Pool.execute('''UPDATE `books`
        SET `name`=%s, isbn=%s, code=%s, price=%s, press=%s, author=%s, pubDate=%s, photo=%s,
            intro=%s, remark=%s, lang=%s, tags=%s, forAge=%s
        WHERE `id`=%s;''', (book['name'], book['isbn'], book['code'], book['price'], book['press'], book['author'], book['pubDate'], book['photo'],
            book['intro'], book['remark'], book['lang'], book['tags'], book['forAge'], bookId))
        self.finish({ 'success': True, 'message': '修改图书成功' })

    @coroutine
    @authenticated
    def delete(self, *args, **kwargs):
        pass


