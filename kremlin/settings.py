# Scrapy settings for kremlin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'kremlin'

SPIDER_MODULES = ['kremlin.spiders']
NEWSPIDER_MODULE = 'kremlin.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'russian-research (+http://www.newcontrarian.com)'
DOWNLOAD_DELAY = 3.0

# FEED_FORMAT = 'csv'
# FEED_URI = 'items.csv'
ITEM_PIPELINES = ['kremlin.pipelines.SQLitePipeline']