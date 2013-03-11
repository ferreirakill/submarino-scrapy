from twisted.internet import reactor
#from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy import log
from submarino_scrapy.spiders.submarino_spider import SubmarinoSpiderSpider
import MySQLdb
import sys
from datetime import datetime, timedelta
from time import localtime, strptime, strftime, mktime

def setup_crawler(origem,destino,ano_saida,mes_saida,dia_saida,ano_chegada,mes_chegada,dia_chegada):
    spider = SubmarinoSpiderSpider(origem=origem,destino=destino,ano_saida=ano_saida,mes_saida=mes_saida,dia_saida=dia_saida,
                                   ano_chegada=ano_chegada,mes_chegada=mes_chegada,dia_chegada=dia_chegada)
    '''
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    '''
    
    #crawlerProcess = Crawler(Settings())
    cp = CrawlerProcess(Settings())
    cp.install()
    cp.configure()
    #crawlerProcess.crawl(spider)
    cp.crawl(spider)
    #crawlerProcess.start()


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
                data_saida=(viagem[1] + timedelta(days=i)).strftime("%Y-%m-%d")
                data_chegada=((viagem[1] + timedelta(days=i)) + timedelta(days=int(viagem[3]))).strftime("%Y-%m-%d")
                
                ano_saida = data_saida.split("-")[0]
                mes_saida = data_saida.split("-")[1]
                dia_saida = data_saida.split("-")[2]
            
                ano_chegada = data_chegada.split("-")[0]
                mes_chegada = data_chegada.split("-")[1]
                dia_chegada = data_chegada.split("-")[2]  
                        
                        
                setup_crawler(origem,destino,ano_saida,mes_saida,dia_saida,ano_chegada,mes_chegada,dia_chegada)
log.start()
reactor.run()