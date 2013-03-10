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

    # Initialization
    def init_request(self):
        import MySQLdb
        import sys
        from datetime import datetime, timedelta
        from time import localtime, strptime, strftime, mktime
        
        def db_connect():
            try:
                conn = MySQLdb.connect (host = "localhost",
                                       user = "root",
                                       passwd = "",
                                       db = "submarino",
                                       port = 4465)
                
                cursor = conn.cursor()
                
            except MySQLdb.Error, e:
                print "Error Connect %d: %s" % (e.args[0], e.args[1])
            
            return cursor,conn
        
        def db_executeQuery(query):
            try:
                cursor,conn = db_connect()
                if query.strip().startswith(("SELECT")):
                    response = cursor.execute (query)
                    return response
                else:
                    cursor.execute (query)
            except MySQLdb.Error, e:
                print "Error Execute %d: %s" % (e.args[0], e.args[1])
                
            finally:
                db_disconnect(cursor,conn)
                #sys.exit (1)
            
                
        def db_disconnect(cursor,conn):
            try:
                cursor.close ()
                conn.commit ()
                conn.close ()
            except MySQLdb.Error, e:
                print "Error Disconnect %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
                
        def getViagem():
            cursor,conn = db_connect()
            select_viagem = """
            SELECT  `id_viagem`,  `data_partida`,  `data_volta`,  `dias_permanecia`,  `range_saida_valor`,  `range_saida_tipo` FROM `submarino`.`viagem` WHERE `ativo` = 'Y';
            """
            cursor.execute(select_viagem)
            response = cursor.fetchall()
            dict_origens = {}
            dict_destinos = {}
            for row in response:
                select_origens = """
                SELECT  `id_origem`,  `id_viagem`,  `sigla_iata` FROM `submarino`.`origem` WHERE `id_viagem` = %s;
                """ % (str(row[0]))
                cursor.execute(select_origens)
                response_origens = cursor.fetchall()
                array_origens = []
        
                for origem in response_origens:
                    array_origens.append(origem[2])
                dict_origens[str(row[0])+'_id_viagem'] = array_origens
                
                select_destinos = """
                SELECT  `id_destino`,  `id_viagem`,  `sigla_iata` FROM `submarino`.`destino` WHERE `id_viagem` = %s;
                """ % (str(row[0]))
                cursor.execute(select_destinos)
                response_destinos = cursor.fetchall()
                array_destinos = []
                for destino in response_destinos:
                    array_destinos.append(destino[2])
                dict_destinos[str(row[0])+'_id_viagem'] = array_destinos        
            
            
            print response
            print dict_origens
            print dict_destinos
            
            return response,dict_origens,dict_destinos
        
        
        def setResultado(origem_iata,destino_iata,cia_aerea,sigla_aerea,preco,data_partida,data_volta):
            cursor,conn = db_connect()
            insert_resultado = """
            INSERT INTO `resultado` (`origem_iata`, `destino_iata`, `cia_aerea`, `sigla_aerea`, `preco`, `data_partida`, `data_volta`) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s');
            """ % (origem_iata,destino_iata,cia_aerea,sigla_aerea,preco,data_partida,data_volta)
            cursor.execute(insert_resultado)
            db_disconnect(cursor,conn)
        
        
        viagens,dict_origens,dict_destinos = getViagem()
        start = time.time()
        for viagem in viagens:
            #(1L, datetime.date(2013, 3, 8), datetime.date(2013, 3, 8), 10L, 3L, 'weeks')
            origens_array=dict_origens[str(viagem[0])+'_id_viagem']
            destinos_array=dict_destinos[str(viagem[0])+'_id_viagem']
            #print origens_array
            #print destinos_array
            if viagem[5].lower().strip().find("weeks")>-1:
                range_saida = range(0,int(viagem[4])*7,7)
            elif viagem[5].lower().strip().find("days")>-1:
                range_saida = range(0,int(viagem[4]))
            else:
                range_saida = range(int(viagem[4]))
            print range_saida
                
            for origem in origens_array:
                for destino in destinos_array:
                    for i in range_saida:
                        dt=(viagem[1] + timedelta(days=i)).strftime("%Y-%m-%d")
                        data_chegada=((viagem[1] + timedelta(days=i)) + timedelta(days=int(viagem[3]))).strftime("%Y-%m-%d")
                        start_requests(self,origem=origem,destino=destino,data_saida=dt,data_chegada=data_chegada)
 
    
    def start_requests(self,origem=origem,destino=destino,data_saida=dt,data_chegada=data_chegada):
        '''
        return [FormRequest("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum",
                        formdata={"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop":"false","Origin":"GRU","Destination":"IBZ","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"08"},{"CiaCodeList":[],"NonStop":"false","Origin":"IBZ","Destination":"GRU","DepartureYear":"2013","DepartureMonth":"04","DepartureDay":"18"}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"}},
                        callback=self.search_id_post)]
        '''
        
        #destino
        "CiaCodeList":[]
        "NonStop":"false"
        "Origin":"GRU"
        "Destination":"IBZ"
        "DepartureYear":"2013"
        "DepartureMonth":"04"
        "DepartureDay":"08"}
        
        #origem
        "CiaCodeList":[]
        "NonStop":"false"
        "Origin":"IBZ"
        "Destination":"GRU"
        "DepartureYear":"2013"
        "DepartureMonth":"04"
        "DepartureDay":"18"
        
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
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
                            "Host": "www.submarinoviagens.com.br",
                            "Cache-Control": "no-cache",
                            "Connection": "Keep-Alive",
                            },
                   callback=self.precos_json, )]
        #pass    
    def precos_json(self, response):
        print response.body
    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = SubmarinoScrapyItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
