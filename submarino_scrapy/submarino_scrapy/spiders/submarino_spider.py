import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from submarino_scrapy.items import SubmarinoScrapyItem
from scrapy.http import FormRequest, Request
import json
import re

class SubmarinoSpiderSpider(CrawlSpider):
    name = 'submarino_spider'
    allowed_domains = ['submarinoviagens.com.br']
    start_urls = ['http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        '''
        return [FormRequest("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum",
                        formdata={"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":"GRU","Destination":"IBZ","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"08"},{"CiaCodeList":[],"NonStop":"false","Origin":"IBZ","Destination":"GRU","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"18"}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"}},
                        callback=self.search_id_post)]
        '''
        return [Request("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum" , method='POST', 
                   body=json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":"GRU","Destination":"IBZ","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"08"},{"CiaCodeList":[],"NonStop":"false","Origin":"IBZ","Destination":"GRU","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"18"}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"}}), 
                   headers={'Content-Type':'application/json',
                            "Accept-Encoding": "gzip: deflate",
                            "Content-Type": "application/json",
                            "x-requested-with": "XMLHttpRequest",
                            "Accept-Language": "pt-br",
                            "Accept": "text/plain: */*",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
                            "Host": "www.submarinoviagens.com.br",
                            "Cache-Control": "no-cache",
                            "Connection": "Keep-Alive",
                            },
                   callback=self.search_id_post, )]
    
    def search_id_post(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        #jsonResponse = json.loads()
        #print response.headers
        uuids = re.findall('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', response.body)
        if len(uuids)<2:
            SubmarinoSpiderSpider(self)
        else:
            print uuids
        
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.body)
        print urls
        return [Request("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/GetSearchStatusJSONMinimum" , method='POST', 
                   body=json.dumps({"req":{"SearchId":uuids[0],"PointOfSale":"SUBMARINO","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"},"pullStatusFrom":"http://" + urls[0]}), 
                   headers={'Content-Type':'application/json',
                            "Accept-Encoding": "gzip: deflate",
                            "Content-Type": "application/json",
                            "x-requested-with": "XMLHttpRequest",
                            "Accept-Language": "pt-br",
                            "Accept": "text/plain: */*",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
                            "Host": "www.submarinoviagens.com.br",
                            "Cache-Control": "no-cache",
                            "Connection": "Keep-Alive",
                            },
                   callback=self.search_id_post, )]
        #pass    
    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = SubmarinoScrapyItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
