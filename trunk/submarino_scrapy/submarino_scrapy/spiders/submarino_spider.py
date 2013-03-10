import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from submarino_scrapy.items import SubmarinoScrapyItem
from scrapy.http import FormRequest, Request
import json

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
                        formdata={"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":"GRU","Destination":"IBZ","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"08"},{"CiaCodeList":[],"NonStop":"false","Origin":"IBZ","Destination":"GRU","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"18"}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":"null"},"HotelSearchData":"null","AttractionSearchData":"null"},"UserSessionId":"","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"}},
                        callback=self.search_id_post)]
        '''
        "http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum"
        return [Request("http://www.submarinoviagens.com.br/Passagens/selecionarvoo?SomenteIda=false&Origem=Sao%20Paulo%20-%20Guarulhos%20/%20SP,%20Brasil,%20Cumbica%20--GRU---&Destino=Ibiza,%20Espanha%20--IBZ---&Origem=Ibiza,%20Espanha%20--IBZ---&Destino=Sao%20Paulo%20-%20Guarulhos%20/%20SP,%20Brasil,%20Cumbica%20--GRU---&Data=08/04/2013&Data=18/04/2013&NumADT=1&NumCHD=0&NumINF=0&SomenteDireto=&Hora=&Hora=&selCabin=&Multi=false" , method='POST', 
                   body=json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":"GRU","Destination":"IBZ","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"08"},{"CiaCodeList":[],"NonStop":"false","Origin":"IBZ","Destination":"GRU","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"18"}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":"null"},"HotelSearchData":"null","AttractionSearchData":"null"},"UserSessionId":"","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"}}), 
                   headers={'Content-Type':'application/json'},
                   callback=self.search_id_post, )]
    
    def search_id_post(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        jsonResponse = json.loads(response.body())
        print jsonResponse
        return jsonResponse
        #pass    
    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = SubmarinoScrapyItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
