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

    #rules = (
    #    Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    #)
    def __init__(self, **kw):
        super(SubmarinoSpiderSpider, self).__init__(**kw)
        origem = kw.get('origem')
        destino = kw.get('destino')
        ano_saida = kw.get('ano_saida')
        mes_saida = kw.get('mes_saida')
        dia_saida = kw.get('ano_saida')
        ano_chegada = kw.get('ano_chegada')
        mes_chegada = kw.get('mes_chegada')
        dia_chegada = kw.get('dia_chegada')  
        user_browser = kw.get('user_browser')  

        self.origem = origem
        self.destino = destino
        self.ano_saida = ano_saida
        self.mes_saida = mes_saida
        self.dia_saida = dia_saida
        self.ano_chegada = ano_chegada
        self.mes_chegada = mes_chegada
        self.dia_chegada = dia_chegada
        self.user_browser = user_browser
        
        #self.url = url
        #self.allowed_domains = [urlparse(url).hostname.lstrip('www.')]
        self.link_extractor = SgmlLinkExtractor()
        self.cookies_seen = set()
        
    # Initialization
    def start_requests(self):
                      
                        '''
                        #destino
                        "CiaCodeList":[]
                        "NonStop":"false"
                        "Origin":"%s"
                        "Destination":"%s"
                        "DepartureYear":"%s"
                        "DepartureMonth":"%s"
                        "DepartureDay":"%s"
                        
                        #origem
                        "CiaCodeList":[]
                        "NonStop":"false"
                        "Origin":"%s"
                        "Destination":"%s"
                        "DepartureYear":"%"
                        "DepartureMonth":"%s"
                        "DepartureDay":"%s"
                         '''
                        print json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":self.origem,"Destination":self.destino,"DepartureYear":self.ano_saida,"DepartureMonth":self.mes_saida,"DepartureDay":self.dia_saida},{"CiaCodeList":[],"NonStop":"false","Origin":self.destino,"Destination":self.origem,"DepartureYear":self.ano_chegada,"DepartureMonth":self.mes_chegada,"DepartureDay":self.dia_chegada}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":self.user_browser}})
                        return [Request("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum" , method='POST',                                         
                                   body=json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":self.origem,"Destination":self.destino,"DepartureYear":self.ano_saida,"DepartureMonth":self.mes_saida,"DepartureDay":self.dia_saida},{"CiaCodeList":[],"NonStop":"false","Origin":self.destino,"Destination":self.origem,"DepartureYear":self.ano_chegada,"DepartureMonth":self.mes_chegada,"DepartureDay":self.dia_chegada}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":self.user_browser}}),
                                   #body=json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":"GRU","Destination":"IBZ","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"08"},{"CiaCodeList":[],"NonStop":"false","Origin":"IBZ","Destination":"GRU","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"18"}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"}}),
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
        
        #urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.body)        
        #print urls
        #"http:\/\/travelengine143.b2w\/TravelEngineWS.svc\"
        
        return [Request("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/GetSearchStatusJSONMinimum" , method='POST', 
                   body=json.dumps({"req":{"SearchId":uuids[0],"PointOfSale":"SUBMARINO","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"},"pullStatusFrom":"http://" + "travelengine143.b2w/TravelEngineWS.svc"}), 
                   headers={'Content-Type':'application/json',
                            "Accept-Encoding": "gzip: deflate",
                            "Content-Type": "application/json",
                            "x-requested-with": "XMLHttpRequest",
                            "Accept-Language": "pt-br",
                            "Accept": "text/plain: */*",
                            "User-Agent": self.user_browser,
                            "Host": "www.submarinoviagens.com.br",
                            "Cache-Control": "no-cache",
                            "Connection": "Keep-Alive",
                            },
                   callback=self.precos_json, )]
        #pass    
    def precos_json(self, response):
        #exec("resposta_parse = " + response.body)
        print json.JSONEncoder().decode(json.loads(response.body))
        #print response.body
    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = SubmarinoScrapyItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
