# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class KremlinItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    post_date = Field()
    text = Field()
    keywords = Field()
    link = Field()
    uid = Field()

class PeemItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    post_date = Field()
    text = Field()
    keywords = Field()
    link = Field()
    uid = Field()