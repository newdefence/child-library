# coding=utf-8
__author__ = 'defence.zhang@gmail.com'
__date__ = "2020/09/14 上午11:38:00"

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(autocommit=True, host="localhost", user="web", passwd="qaz123", db="child_library")
cursor = conn.cursor()

cursor.execute('SELECT * FROM books LIMIT 1;')
print cursor.fetchall()


conn.close()
