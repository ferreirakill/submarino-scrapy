# This snippet can be used to run scrapy spiders independent of scrapyd or the scrapy command line tool and use it from a script. 
# 
# The multiprocessing library is used in order to work around a bug in Twisted, in which you cannot restart an already running reactor or in this case a scrapy instance.
# 
# [Here](http://groups.google.com/group/scrapy-users/browse_thread/thread/f332fc5b749d401a) is the mailing-list discussion for this snippet. 

#!/usr/bin/python
import os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'submarino_scrapy.settings') #Must be at the top before other import

from scrapy import log, signals, project
from scrapy.xlib.pydispatch import dispatcher
#from scrapy.conf import settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue
from submarino_scrapy.spiders.submarino_spider import SubmarinoSpiderSpider

class CrawlerScript():

    def __init__(self):
        self.crawler = CrawlerProcess(Settings())
        #self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def _crawl(self, queue, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        if spider:
            self.crawler.queue.append_spider(spider)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)
    
    def crawl(self, spider):
        queue = Queue()
        p = Process(target=self._crawl, args=(queue, spider,))
        p.start()
        p.join()
        return queue.get(True)

# Usage
if __name__ == "__main__":
    log.start()
    
    """
    This example runs spider1 and then spider2 three times. 
    """
    items = list()
    crawler = CrawlerScript()
    #items.append(crawler.crawl('SubmarinoSpiderSpider'))
    spider = SubmarinoSpiderSpider(origem='GRU',destino='LHR',ano_saida='2013',mes_saida='04',dia_saida='17',ano_chegada='2013',mes_chegada='04',dia_chegada='22',user_browser="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0")
    for i in range(3):
        items.append(crawler.crawl('SubmarinoSpider'))
    print items

# Snippet imported from snippets.scrapy.org (which no longer works)
# author: joehillen
# date  : Oct 24, 2010
