# Scrapy settings for submarino_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'submarino_scrapy'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['submarino_scrapy.spiders']
NEWSPIDER_MODULE = 'submarino_scrapy.spiders'
DEFAULT_ITEM_CLASS = 'submarino_scrapy.items.SubmarinoScrapyItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

