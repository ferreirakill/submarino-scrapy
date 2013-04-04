# Scrapy settings for submarino_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'submarino_scrapy'
#BOT_VERSION = '1.0'

SPIDER_MODULES = ['submarino_scrapy.spiders']
NEWSPIDER_MODULE = 'submarino_scrapy.spiders'
DEFAULT_ITEM_CLASS = 'submarino_scrapy.items.SubmarinoScrapyItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"

RETRY_ENABLED = True
RETRY_TIMES = 50
RETRY_HTTP_CODES = [400,]
COOKIES_DEBUG = True

LOG_ENABLED = True
LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    #'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
    #'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
    #'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    #'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'submarino_scrapy.middlewares.RetryMiddleware': 500,
    #'submarino_scrapy.middlewares.RepeatMiddleware': 530,
    #'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
    #'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
    #'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
    #'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
    #'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
    #'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
    #'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
    #'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
}