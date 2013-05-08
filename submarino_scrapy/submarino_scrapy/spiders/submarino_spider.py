
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from submarino_scrapy.items import SubmarinoScrapyItem
from scrapy.http import FormRequest, Request
from twisted.internet.error import TimeoutError as ServerTimeoutError, DNSLookupError, \
                                   ConnectionRefusedError, ConnectionDone, ConnectError, \
                                   ConnectionLost, TCPTimedOutError
import json
import re
import ast
import traceback
import sys
import time
import random

import MySQLdb
import sys
from datetime import datetime, timedelta
import random, time
from time import localtime, strptime, strftime, mktime
from random import choice

import atexit

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


def setResultado(origem_iata,destino_iata,cia_aerea,sigla_aerea,preco,data_partida,data_volta,id_viagem=1):
    cursor,conn = db_connect()
    insert_resultado = """
    INSERT INTO `resultado` (`origem_iata`, `destino_iata`, `cia_aerea`, `sigla_aerea`, `preco`, `data_partida`, `data_volta`, `id_viagem`) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s', %s);
    """ % (origem_iata,destino_iata,cia_aerea,sigla_aerea,preco,data_partida,data_volta,id_viagem)
    cursor.execute(insert_resultado)
    db_disconnect(cursor,conn)

def get_proxy_random():
    cursor,conn = db_connect()
    select_trade = """
    select INET_NTOA(IP) as ip_conv,Port from stocks_db.proxies_list where ativo = 'Y' and response < 20 and response is not NULL ORDER BY RAND() LIMIT 1;
    """
    cursor.execute(select_trade)
    response = cursor.fetchall()
    for row in response:
        proxy_rand = (str(row[0])+":"+str(row[1]))
        
    return proxy_rand
    
def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value):
                yield subvalue
    else:
        yield o
     

def emailHtmlSet(title, sql):
    
    #date_now = datetime.now() - timedelta(minutes=(gmt_offset_brazil)) #gmtoffset (brazil time)
    date_now = datetime.now()
    #now_report = datetime.now().strftime("%H:%M") 
    #str_now_report = strftime("%H:%M", strptime(now_report, "%H:%M"))
    
    # Prepare report
    output = []
    
    output.append("<html>")
    output.append('<head><style type="text/css">')
    output.append('body,tr{font-family:Verdana,Tahoma,Arial;font-size:10pt}')
    output.append('.cmp{background-color:#FF9933;font-weight:bold;font-size:11pt;text-align:center}')
    output.append('th{background-color:#FFCC33;font-weight:bold;text-align:center}')
    output.append('td{background-color:#FFFF99;text-align:center}</style></head><body><center>')    
    
    output.append("<h2>%s</h2>" % (title))
    output.append("<h3>Data: %s</h3><br>" % date_now)
               
    try:
        cursor,conn = db_connect()
        cursor.execute(sql)
        sql_response = cursor.fetchall()        
        output.append('<table border="0" cellspacing="1" bgcolor="#666666">')                         
        if(len(sql_response)>0):
            output.append('<tr>')                
            field_names  = cursor.description
            for field_names_item in field_names:
                output.append('<th width="100px">%s</th>' % field_names_item[0])            
            output.append('</tr>')                
            for sql_response_row in sql_response:
                output.append('<tr>')
                for sql_response_row_field in sql_response_row:
                    output.append('<td>%s</td>' % sql_response_row_field)
                output.append('</tr>')
        else:
            output.append('<tr>')
            output.append('<td width="100%">')
            output.append('0 rows returned!')
            output.append('</td>')
            output.append('</tr>')
        output.append("</table><br>")
        
    except:
        #Query error response!                
        output.append("<h4>SQL EXECUTER</h4><br>")
        output.append('<table width="100%" border="0" cellspacing="1" bgcolor="#666666">')                
        output.append('<tr width="100%">')
        output.append('<td style="text-align:left;" width="100%">')
        output.append('Query error response!<br><br>')
        output.append("Unexpected error: %s" % sys.exc_info()[0])                 
        output.append("<br><br>SQL: %s" % sql)                                        
        output.append('</td>')
        output.append('</tr>')
        output.append("</table><br>")
        #Print the traceback for a detailed error description!
        #print "An unhandled exception occured, here's the traceback!" 
        traceback.print_exc()
    finally:
        db_disconnect(cursor,conn)
    
       
        
    output.append("</html>")
    html_mail = "".join(output)
    return(html_mail)  
        
def sendMail(you, subject, message):    
    import smtplib
    
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    # me == my email address
    # you == recipient's email address
    me = "wchaves@gmail.com"
    #you = "your@email.com"
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    
    # Create the body of the message (a plain-text and an HTML version).
    text = "Se nao consegue visualizar, favor habilitar o recebimento de emails HTML!"
    html = message
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()    

def get_emails_viagem():
    cursor,conn = db_connect()
    select_emails = """
    select distinct(email) from submarino.viagem where ativo = 'Y';
    """
    cursor.execute(select_emails)
    response = cursor.fetchall()
        
    return response

@atexit.register
def reportBeforeExit():
    print "...enviando email...."
    title = 'RESULTADOS DA BUSCA DE HOJE'
    emails_addresses = get_emails_viagem()
    for email in emails_addresses:
        sql = '''
            select C.origem_iata as Origem_Iata, C.airport as Origem, C.destino_iata as Destino_Iata, D.airport as Destino, C.cia_aerea, MIN(C.preco) ,C.data_partida,C.data_volta,C.updated, C.email from 
            (select A.id_viagem as id_vi,A.origem_iata, A.destino_iata, A.cia_aerea, A.preco,A.data_partida,A.data_volta,A.updated, B.airport, E.email from resultado A
                inner join iata_airport_codes B
                on A.origem_iata = B.code
                inner join viagem E
                on E.id_viagem = A.id_viagem
                    WHERE E.email = '%s'
                    AND DATE(A.updated) = DATE(NOW())) C inner join iata_airport_codes D 
            on C.destino_iata = D.code
            GROUP BY C.origem_iata, C.destino_iata
            order by preco ASC
            ''' % (email[0])
        message = emailHtmlSet(title, sql)
        #sendMail(email[0], 'Robo de passagens - Ultimos Resultados', message)
        sendMail('wchaves@gmail.com', 'Robo de passagens - Ultimos Resultados', message)
    print "Email enviado!"       
        
def remover_acentos(txt, codif='utf-8'):
    from unicodedata import normalize
    return normalize('NFKD', txt.decode(codif, "ignore")).encode('ASCII','ignore')
        
class SubmarinoSpiderSpider(CrawlSpider):
    name = 'submarino_spider'
    allowed_domains = ['submarinoviagens.com.br']
    #start_urls = ['http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum']
    start_urls = []
    viagem_combina = []

    #rules = (
    #    Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    #)
    def __init__(self, **kw):
        super(SubmarinoSpiderSpider, self).__init__(**kw)
        
        #####################################################
        #####################################################
        ####GETTING ALL POSSIBLE TRAVEL DESTINATIONS    #####
        #####################################################
        #####################################################
        viagens,dict_origens,dict_destinos = getViagem()
        #viagem = viagens[0]
        for viagem in viagens:
            
            origens_array=dict_origens[str(viagem[0])+'_id_viagem']
            destinos_array=dict_destinos[str(viagem[0])+'_id_viagem']
            
            #para viagens com range de dias ou semanas diferentes.
            if viagem[3].find("-")>-1:
                permanencia_maior = int(viagem[3].split("-")[-1])
                permanencia_menor = int(viagem[3].split("-")[0])
                permanencia_diff = range(permanencia_menor,(permanencia_maior+1))
            else:
                permanencia_maior = int(viagem[3])
                permanencia_diff = range(permanencia_maior,(permanencia_maior+1))
            
            for permanencia_atual in permanencia_diff:
                
                if viagem[5].lower().strip().find("weeksfw")>-1:
                    range_saida = range(0,int(viagem[4])*7,7)
                elif viagem[5].lower().strip().find("weeksbehind")>-1:
                    range_saida = range(int(viagem[4])*(-7),7,0)
                elif viagem[5].lower().strip().find("weeks")>-1:
                    range_saida = range(int(viagem[4])*(-7),int(viagem[4])*7,7)            
                elif viagem[5].lower().strip().find("daysfw")>-1:
                    range_saida = range(0,int(viagem[4]))
                elif viagem[5].lower().strip().find("daysbehind")>-1:
                    range_saida = range(((-1)*int(viagem[4])),0)
                elif viagem[5].lower().strip().find("days")>-1:
                    range_saida = range(((-1)*int(viagem[4])),int(viagem[4]))            
                else:
                    range_saida = range(int(viagem[4]))
                
                print "range_saida= %s" % (range_saida)
                
                for origem in origens_array:
                #for origem in origens_array[:1]: ###TESTE###
                    for destino in destinos_array:
                    #for destino in destinos_array[:1]: ###TESTE###
                        for i in range_saida:
                        #for i in range_saida[:5]: ###TESTE###
                        
                            ##tipos de range###
                            #fixedgo - Dia fixo de saida.
                            #fixedback - Dia fixo da volta
                            #fixed perm - Tempo de Permanencia fixo
                            #daysfw - Range dias pra frente
                            #daysbehind - Range dias pra tras
                            #days - Dias Ambos os lados
                            #weeksfw - Range semanas pra frente
                            #weeksbehind - Range semanas pra tras
                            #weeks - Semanas Ambos os lados                    
                            
                            if viagem[5].lower().strip().find("fixedgo")>-1:
                                data_saida=(viagem[1]).strftime("%Y-%m-%d")
                            else:
                                data_saida=(viagem[1] + timedelta(days=i)).strftime("%Y-%m-%d")
                                
                            if viagem[5].lower().strip().find("fixedback")>-1:
                                if ((viagem[1] + timedelta(days=i)) > (viagem[2])):
                                    print "Ida depois da volta! Break!"
                                    break
                                else:
                                    data_chegada=(viagem[2]).strftime("%Y-%m-%d")
                            else:
                                data_chegada=((viagem[1] + timedelta(days=i)) + timedelta(days=permanencia_atual)).strftime("%Y-%m-%d")
                            
                            ano_saida = data_saida.split("-")[0]
                            mes_saida = data_saida.split("-")[1]
                            dia_saida = data_saida.split("-")[2]
                        
                            ano_chegada = data_chegada.split("-")[0]
                            mes_chegada = data_chegada.split("-")[1]
                            dia_chegada = data_chegada.split("-")[2] 
                            
                            self.viagem_combina.append({'id_viagem':int(viagem[0]),
                                                    'ano_saida':ano_saida,
                                                   'mes_saida':mes_saida,
                                                   'dia_saida':dia_saida,
                                                   'ano_chegada':ano_chegada,
                                                   'mes_chegada':mes_chegada,
                                                   'dia_chegada':dia_chegada,
                                                   'origem':origem,
                                                   'destino':destino,
                                                   'data_saida':data_saida,
                                                   'data_chegada':data_chegada,
                                                   })

        #print self.viagem_combina
        print "Quantidade de combinacoes: %s" % len(self.viagem_combina)
        
        '''                      
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
        
        self.origem = 'GRU'
        self.destino = 'MAD'
        self.ano_saida = '2013'
        self.mes_saida = '04'
        self.dia_saida = '14'
        self.ano_chegada = '2013'
        self.mes_chegada = '04'
        self.dia_chegada = '25'
        self.user_browser = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"
        '''

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
        requests_arr = []
        if len(self.viagem_combina)>0:
            for i in range(len(self.viagem_combina)):
                print "viagem_combina: %s" % (self.viagem_combina[i])
                self.id_viagem = self.viagem_combina[i].get('id_viagem')
                self.origem = self.viagem_combina[i].get('origem')
                self.destino = self.viagem_combina[i].get('destino')
                self.ano_saida = self.viagem_combina[i].get('ano_saida')
                self.mes_saida = self.viagem_combina[i].get('mes_saida')
                self.dia_saida = self.viagem_combina[i].get('dia_saida')
                self.ano_chegada = self.viagem_combina[i].get('ano_chegada')
                self.mes_chegada = self.viagem_combina[i].get('mes_chegada')
                self.dia_chegada = self.viagem_combina[i].get('dia_chegada')  
                #user_browser = self.viagem_combina[i].get('user_browser')
                self.user_browser =  random_header()
                #self.viagem_combina.pop(0)      
                print "%s - %s" % (i,json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop": False,"Origin":self.origem,"Destination":self.destino,"DepartureYear":self.ano_saida,"DepartureMonth":self.mes_saida,"DepartureDay":self.dia_saida},{"CiaCodeList":[],"NonStop":"false","Origin":self.destino,"Destination":self.origem,"DepartureYear":self.ano_chegada,"DepartureMonth":self.mes_chegada,"DepartureDay":self.dia_chegada}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":self.user_browser}}))
                
                request_prep = Request('http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum', 
                                        method='POST',                                         
                                        body=json.dumps({"req":{"PointOfSale":"SUBMARINO","SearchData":{"SearchMode":1,"AirSearchData":{"CityPairsRequest":[{"CiaCodeList":[],"NonStop": False,"Origin":self.origem,"Destination":self.destino,"DepartureYear":self.ano_saida,"DepartureMonth":self.mes_saida,"DepartureDay":self.dia_saida},{"CiaCodeList":[],"NonStop":"false","Origin":self.destino,"Destination":self.origem,"DepartureYear":self.ano_chegada,"DepartureMonth":self.mes_chegada,"DepartureDay":self.dia_chegada}],"NumberADTs":1,"NumberCHDs":0,"NumberINFs":0,"SearchType":1,"CabinFilter":None},"HotelSearchData":None,"AttractionSearchData":None},"UserSessionId":"","UserBrowser":self.user_browser}}),                             
                                        headers={'Content-Type':'application/json',
                                                 "Accept-Encoding": "gzip: deflate",
                                                 "x-requested-with": "XMLHttpRequest",
                                                 "Accept-Language": "pt-br",
                                                 "Accept": "text/plain: */*",
                                                 "User-Agent": self.user_browser,
                                                 "Host": "www.submarinoviagens.com.br",
                                                 "Cache-Control": "no-cache",
                                                 "Connection": "Keep-Alive",
                                                 },
                                        callback=self.get_uuid_param, )
                request_prep.meta['id_viagem_array'] = i
                #request_prep.meta['proxy'] = 'http://' + get_proxy_random()
                #print "Proxy: %s" % (request_prep.meta['proxy']) 
                requests_arr.append(request_prep)  
        
        
        return requests_arr
        
    def get_uuid_param(self,response):
        #print "..sleeping"
        #time.sleep(random.randint(1, 5))
        #print "..waking"
        
        #print "response.body: %s" % (response.body)
        
        uuids = re.findall('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', response.body)
        
        try:
            if not uuids[0]=='00000000-0000-0000-0000-000000000000':
                
                
                #origem_nome = preco_list[1][0][2][0][0] #origem nome
                #destino_nome = preco_list[1][0][2][0][0] #destino nome
                i = response.meta['id_viagem_array']
                #print "Proxy Response: %s" % (response.meta['proxy'])
                print "viagem_combina: %s" % (self.viagem_combina[i])
                
                id_viagem = self.viagem_combina[i].get('id_viagem')
                origem = self.viagem_combina[i].get('origem')
                destino = self.viagem_combina[i].get('destino')
                ano_saida = self.viagem_combina[i].get('ano_saida')
                mes_saida = self.viagem_combina[i].get('mes_saida')
                dia_saida = self.viagem_combina[i].get('dia_saida')
                ano_chegada = self.viagem_combina[i].get('ano_chegada')
                mes_chegada = self.viagem_combina[i].get('mes_chegada')
                dia_chegada = self.viagem_combina[i].get('dia_chegada')  
                
                data_saida = self.viagem_combina[i].get('data_saida')
                data_chegada = self.viagem_combina[i].get('data_chegada')
                
                print "ID:%s  %s-%s (%s)-(%s)" % (i,origem,destino,data_saida,data_chegada)
                
                '''                
                origem = preco_list[1][0][2][0][1] #origem IATA
                destino = preco_list[1][0][1][0][1] #destino IATA
                
                ano_saida = preco_list[1][0][7][-1]
                mes_saida = preco_list[1][0][7][-2]
                dia_saida = preco_list[1][0][7][0]
                
                ano_chegada = preco_list[1][0][6][-1]
                mes_chegada = preco_list[1][0][6][-2]
                dia_chegada = preco_list[1][0][6][0]
                '''
                      
                #Melhor preco em dollars
                #print "Melhor Preco Dollars: %s" % (preco_list[1][0][17])
                #Melhor preco em reais
                #print "Melhor Preco Reais: %s" % (preco_list[1][0][18])
                
                #Melhor preco por escalas
                #print "Melhor Preco Voo Direto: %s" % (preco_list[1][0][21][0])
                #print "Melhor Preco Voo 1 Escala: %s" % (preco_list[1][0][21][1])
                #print "Melhor Preco Voo 2 Escalas: %s" % (preco_list[1][0][21][2])
                try:
                    preco_list = json.JSONDecoder().decode(json.loads(response.body))
                    for air in preco_list[1][0][0]:
                        print "Sigla Compania: %s" % (air[0])
                        #print "Nome Compania: %s" % (remover_acentos(air[1]))
                        print "Preco Compania: %s" % (air[2])
                        #print "XXX Compania: %s" % (air[3])
                        try:
                            setResultado(origem,destino,air[1],air[0],air[2],
                                         (str(ano_saida) + '-' + str(mes_saida) + '-' + str(dia_saida)),
                                         (str(ano_chegada) + '-' + str(mes_chegada) + '-' + str(dia_chegada)),int(id_viagem)
                                        )
                        except MySQLdb.IntegrityError as err:
                            print "Resultado Jah existe no Banco, passa!"
                            print err
                            pass
                except:
                    print "Exception KeyError!"
                    
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,
                          limit=2, file=sys.stdout)
                                   
                    request_b = Request("http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/GetSearchStatusJSONMinimum" , method='POST', 
                       body=json.dumps({"req":{"SearchId":uuids[0],"PointOfSale":"SUBMARINO","UserBrowser":self.user_browser},"pullStatusFrom":"http://travelengine143.b2w/TravelEngineWS.svc"}), 
                       headers={'Content-Type':'application/json',
                                "Accept-Encoding": "gzip: deflate",
                                "x-requested-with": "XMLHttpRequest",
                                "Accept-Language": "pt-br",
                                "Accept": "text/plain: */*",
                                "User-Agent": self.user_browser,
                                "Host": "www.submarinoviagens.com.br",
                                "Cache-Control": "no-cache",
                                "Connection": "Keep-Alive",
                                }, 
                                callback=self.get_uuid_param, )
                    #request_b.meta['proxy'] = response.meta['proxy']
                    return request_b
                            

        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,
                  limit=2, file=sys.stdout)
    