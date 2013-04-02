from scrapy import signals, log
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.http import Request
from submarino_scrapy.spiders.submarino_spider import SubmarinoSpiderSpider

def handleSpiderIdle(spider):
    '''Handle spider idle event.''' # http://doc.scrapy.org/topics/signals.html#spider-idle
    print '\nSpider idle: %s. Restarting it... ' % spider.name
    for url in spider.start_urls: # reschedule start urls
        spider.crawler.engine.crawl(Request(url, dont_filter=True), spider)

mySettings = {'LOG_ENABLED': True} # global settings http://doc.scrapy.org/topics/settings.html

Settings().overrides.update(mySettings)

crawlerProcess = CrawlerProcess(Settings())
crawlerProcess.install()
crawlerProcess.configure()

spider = SubmarinoSpiderSpider(origem='GRU',destino='LHR',ano_saida='2013',mes_saida='04',dia_saida='17',ano_chegada='2013',mes_chegada='04',dia_chegada='22',user_browser="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0") # create a spider ourselves
#crawlerProcess.queue.append_spider(spider) # add it to spiders pool
crawlerProcess.engine.open_spider(spider)

dispatcher.connect(handleSpiderIdle, signals.spider_idle) # use this if you need to handle idle event (restart spider?)

log.start() # depends on LOG_ENABLED
print "Starting crawler."
crawlerProcess.start()
print "Crawler stopped."