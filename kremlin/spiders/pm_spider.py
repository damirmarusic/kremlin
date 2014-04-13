from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from kremlin.items import PeemItem

import sqlite3
import re
import datetime as dtm
import locale

class PMSpider(BaseSpider):
    name = "peem"
    allowed_domains = ["government.ru"]
    r_url = 'http://government.ru/news/'
    s_url = '/reader'
    uids = range(2838)
    start_urls = [r_url + str(uid) + s_url for uid in uids]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = PeemItem()
        item['title'] = hxs.select('//h3[@class="reader_article_headline"]/text()').extract()[0].strip()
        item['text'] = '\n\n'.join(hxs.select('//div[@class="reader_article_body"]/p/text()').extract()).strip()
        item['link'] = response.url
        post_date = hxs.select('//span[@class="reader_article_dateline__date"]/text()').extract()[0].strip()
        locale.setlocale(locale.LC_ALL,'ru_RU.UTF-8')
        rdate = dtm.datetime.strptime(post_date.encode('UTF-8'), '%d %B %Y')
        item['post_date'] = rdate.strftime('%Y') + '-' + rdate.strftime('%m') + '-' + rdate.strftime('%d')
        item['keywords'] = ''
        return item