#from scrapy.conf import settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from submarino_scrapy.spiders.submarino_spider import SubmarinoSpiderSpider
import MySQLdb
import sys
from datetime import datetime, timedelta
import random, time
from time import localtime, strptime, strftime, mktime
from random import choice

from scrapy import project, signals
from scrapy.xlib.pydispatch import dispatcher
import multiprocessing
import Queue
from twisted.internet import reactor
from scrapy import log

#WORKERS = 30

def random_header():
    browser_headers = ['Opera/9.51 (Macintosh; Intel Mac OS X; U; en)',
                        'Opera/9.70 (Linux i686 ; U; en) Presto/2.2.1',
                        'Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.2.15 Version/10.00',
                        'Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01',
                        'Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00',
                        'Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01',
                        'Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10',
                        'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.0; it-IT; rv:1.7.12) Gecko/20050915',
                        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.0.1) Gecko/20020919',
                        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5',
                        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2',
                        'Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5',
                        'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8',
                        'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3',
                        'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5',
                        'Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2',
                        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4',
                        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre',
                        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre',
                        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre',
                        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre',
                        'Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2',
                        'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
                        'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4',
                        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10',
                        'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14',
                        'Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
                        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1',
                        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
                        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
                        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
                        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
                        'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10',
                        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.10 Chromium/16.0.912.21 Chrome/16.0.912.21 Safari/535.7',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.04 Chromium/15.0.871.0 Chrome/15.0.871.0 Safari/535.2',
                        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/10.04 Chromium/14.0.813.0 Chrome/14.0.813.0 Safari/535.1',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
                        'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10',
                        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fi-fi) AppleWebKit/420+ (KHTML, like Gecko) Safari/419.3',
                        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.7',
                        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.6',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; cs-CZ) AppleWebKit/523.15 (KHTML, like Gecko) Version/3.0 Safari/523.15',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_6; it-it) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
                        'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT;)',
                        'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
                        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0)',
                        'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)',
                        'Mozilla/4.0 (compatible; MSIE 5.0b1; Mac_PowerPC)',
                        'Mozilla/2.0 (compatible; MSIE 4.0; Windows 98)',
                        'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT)',
                        'Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; GTB6; Ant.com Toolbar 1.6; MSIECrawler)',
                        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET CLR 3.0.30729)',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)',
                        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',]

    return choice(browser_headers)

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


    '''   
    for row in range(len(origens_array)):

        for j in range(len(destinos_array)):
            
            for i in range_saida:
                
                data_saida=(viagem[1] + timedelta(days=i)).strftime("%Y-%m-%d")
                data_chegada=((viagem[1] + timedelta(days=i)) + timedelta(days=int(viagem[3]))).strftime("%Y-%m-%d")
                
                ano_saida = data_saida.split("-")[0]
                mes_saida = data_saida.split("-")[1]
                dia_saida = data_saida.split("-")[2]
            
                ano_chegada = data_chegada.split("-")[0]
                mes_chegada = data_chegada.split("-")[1]
                dia_chegada = data_chegada.split("-")[2]  
                   
                queue.put([
                            origens_array[row], #origem
                            destinos_array[j], #destino
                            ano_saida,
                            mes_saida,
                            dia_saida,
                            ano_chegada,
                            mes_chegada,
                            dia_chegada,                            
                           ])
    '''
            
    

        
class CrawlerWorker(multiprocessing.Process):
 
    def __init__(self, spider, work_queue, result_queue):
 
        # base class initialization
        multiprocessing.Process.__init__(self)
 
        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False
        

        self.spider = spider
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)        
 
    def _item_passed(self, item):
        self.items.append(item)   
        
    def run(self):
        while not self.kill_received:
 
            # get a task
            #job = self.work_queue.get_nowait()
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                break
 
            # the actual processing
            print("Starting " + str(job) + " ...")
            delay = random.randrange(1,3)
            time.sleep(delay)
            

            self.spider.engine.open_spider(self.spider)
            #self.spider.engine.crawl(self.spider)
            
            #reactor.run()
            #self.crawler.stop()
            #reactor.stop()
            #self.crawler.uninstall()
            # store the result
            self.result_queue.put(self.items)

if __name__ == "__main__":
    
    viagens,dict_origens,dict_destinos = getViagem()
    viagem = viagens[0]
    origens_array=dict_origens[str(viagem[0])+'_id_viagem']
    destinos_array=dict_destinos[str(viagem[0])+'_id_viagem']
    
    if viagem[5].lower().strip().find("weeks")>-1:
        range_saida = range(0,int(viagem[4])*7,7)
    elif viagem[5].lower().strip().find("days")>-1:
        range_saida = range(0,int(viagem[4]))
    else:
        range_saida = range(int(viagem[4]))
                
    #num_jobs = len(origens_array)*len(destinos_array)*len(range_saida)
    num_jobs = 1
    num_processes=1
 
    # run
    # load up work queue
    work_queue = multiprocessing.Queue()
    #for job in range(num_jobs):
    #    work_queue.put(job)
    
    
    # crawler settings
    crawler = CrawlerProcess(Settings())
    #if not hasattr(project, 'crawler'):
    #    crawler.install()
    crawler.configure()     
    
    #for origem in origens_array:
    for origem in origens_array[:1]: ###TESTE###
        #for destino in destinos_array:
        for destino in destinos_array[:1]: ###TESTE###
            #for i in range_saida:
            for i in range_saida[:1]: ###TESTE###
                data_saida=(viagem[1] + timedelta(days=i)).strftime("%Y-%m-%d")
                data_chegada=((viagem[1] + timedelta(days=i)) + timedelta(days=int(viagem[3]))).strftime("%Y-%m-%d")
                
                ano_saida = data_saida.split("-")[0]
                mes_saida = data_saida.split("-")[1]
                dia_saida = data_saida.split("-")[2]
            
                ano_chegada = data_chegada.split("-")[0]
                mes_chegada = data_chegada.split("-")[1]
                dia_chegada = data_chegada.split("-")[2] 
                
                work_queue.put(origem+"_"+destino+"_"+data_saida+"_"+data_chegada)

    log.start()
    crawler.start() 
    reactor.run()
    # create a queue to pass to workers to store the results
    result_queue = multiprocessing.Queue()
 
    # spawn workers
    for i in range(num_processes):
        worker = CrawlerWorker(SubmarinoSpiderSpider(origem=origem,destino=destino,ano_saida=ano_saida,mes_saida=mes_saida,dia_saida=dia_saida, ano_chegada=ano_chegada,mes_chegada=mes_chegada,dia_chegada=dia_chegada,user_browser=random_header()), work_queue, result_queue)
        worker.start()
 
    # collect the results off the queue
    results = []
    for i in range(num_jobs):
        print(result_queue.get())                