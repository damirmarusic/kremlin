# Define your item pipelines here

from scrapy import log
from twisted.enterprise import adbapi

import time
import pymysql.cursors

import sqlite3

class SQLitePipeline(object):

    def __init__(self):
        log.start('logfile')
        self.conn = sqlite3.connect('russia.db')
        self.c = self.conn.cursor()
        query = ''' CREATE TABLE IF NOT EXISTS kremlin(id INTEGER PRIMARY KEY, title TEXT, 
                    body TEXT, keywords TEXT, post_date DATE, 
                    link TEXT) '''
        self.c.execute(query)

    def process_item(self, item, spider):
        self.c.execute("SELECT * FROM kremlin WHERE link = ?", (item['link'],))
        result = self.c.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            self.c.execute(\
                "INSERT INTO kremlin (title, body, keywords, post_date, link) "
                "VALUES (?, ?, ?, ?, ?)", 
                (item['title'], item['text'], item['keywords'], item['post_date'], item['link'])
                )
            self.conn.commit()
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)

class MySQLStorePipeline(object):

    def __init__(self):
        log.start('logfile')
        self.dbpool = adbapi.ConnectionPool('pymysql',
                db='russia',
                user='kremlinology',
                passwd='#?!russia666!',
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        tx.execute("select * from kremlin where uid = %s", (item['uid']))
        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            tx.execute(\
                "insert into kremlin (uid, title, body, keywords, post_date, link) "
                "values (%s, %s, %s, %s, %s, %s)",
                (item['uid'],
                 item['title'],
                 item['text'],
                 item['keywords'],
                 item['post_date'],
                 item['link'])
            )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
