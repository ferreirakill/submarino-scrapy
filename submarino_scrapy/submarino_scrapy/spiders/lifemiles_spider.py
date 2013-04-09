
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
#from submarino_scrapy.items import SubmarinoScrapyItem
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
import urllib

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


        
class LifemilesSpiderSpider(CrawlSpider):
    name = 'lifemiles_spider'
    allowed_domains = ['lifemiles.com']
    #start_urls = ['http://www.submarinoviagens.com.br/Passagens/UIService/Service.svc/SearchGroupedFlightsJSONMinimum']
    start_urls = []
    viagem_combina = []

    #rules = (
    #    Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    #)
    def __init__(self, **kw):
        super(LifemilesSpiderSpider, self).__init__(**kw)
        
        self.link_extractor = SgmlLinkExtractor()
        self.cookies_seen = set()
        
    # Initialization
    def start_requests(self):
        self.user_browser =  random_header()
        return [Request('http://www.lifemiles.com/lib/ajax/ENG/getSession.aspx', 
                                method='GET',
                                body=urllib.urlencode({'user':'wchaves@gmail.com',
                                      'pass':'Wymwtb24',
                                      }),   
                                headers={'Content-Type':'text/html; charset=utf-8',
                                         "x-requested-with": "XMLHttpRequest",
                                         "Accept-Encoding": "gzip: deflate",
                                         "Accept-Language": "en-US,en;q=0.5",
                                         "Accept": "text/html, */*",
                                         "User-Agent": self.user_browser,
                                         "Host": "www.lifemiles.com",
                                         "Connection": "Keep-Alive",
                                         "Referer": "https://www.lifemiles.com/eng/use/red/dynrederr.aspx?&ls=76676653&rr=4",
                                         },
                                callback=self.after_signin, )]
        
    def after_signin(self,response):
        
        print response.body
        
        #return [FormRequest.from_response(response,
        #            formdata={'username': 'john', 'password': 'secret'},
        #            callback=self.after_login)]
        return [Request('https://www.lifemiles.com/eng/use/red/dynredcal.aspx', 
                                method='POST',
                                body={
                                    'CmbPaxNum':'1',
                                    'cabin':'Y',
                                    'cmbDestino':'JFK',
                                    'cmbDestino1':'-1',
                                    'cmbDestino2':'-1',
                                    'cmbDestino3':'-1',
                                    'cmbDestino4':'-1',
                                    'cmbDestino5':'-1',
                                    'cmbDestino6':'-1',
                                    'cmbDestino7':'-1',
                                    'cmbDestino8':'-1',
                                    'cmbOrigen':'GRU',
                                    'cmbOrigen1':'-1',
                                    'cmbOrigen2':'-1',
                                    'cmbOrigen3':'-1',
                                    'cmbOrigen4':'-1',
                                    'cmbOrigen5':'-1',
                                    'cmbOrigen6':'-1',
                                    'cmbOrigen7':'-1',
                                    'cmbOrigen8':'-1',
                                    'cmbSocAe':'TA',
                                    'fechaRegreso':'06/08/2013',
                                    'fechaSalida':'06/01/2013',
                                    'fechaSalida1':'',
                                    'fechaSalida2':'',
                                    'fechaSalida3':'',
                                    'fechaSalida4':'',
                                    'fechaSalida5':'',
                                    'fechaSalida6':'',
                                    'fechaSalida7':'',
                                    'fechaSalida8':'',
                                    'hidCSocio':'TA',
                                    'hidItineraryType':'2',
                                    'hidRedemptionType':'1',
                                    'hidinput':'textDestino',
                                    'hidlength':'',
                                    'horaRegreso':'0000',
                                    'horaSalida':'0000',
                                    'horaSalida1':'0000',
                                    'horaSalida2':'0000',
                                    'horaSalida3':'0000',
                                    'horaSalida4':'0000',
                                    'horaSalida5':'0000',
                                    'horaSalida6':'0000',
                                    'horaSalida7':'0000',
                                    'horaSalida8':'0000',
                                    'promoCode':'',
                                    'text':'Sao Paulo (GRU), Brazil',
                                    'text':'New York (JFK), United States',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',
                                    'text':'Origin',
                                    'text':'Destination',                                        
                                      },                                    
                                headers={'Content-Type':'text/html; charset=utf-8',
                                         "Accept-Encoding": "gzip: deflate",
                                         "Accept-Language": "en-US,en;q=0.5",
                                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                         "User-Agent": self.user_browser,
                                         "Host": "www.lifemiles.com",
                                         "Connection": "Keep-Alive",
                                         "Referer": "    https://www.lifemiles.com/eng/use/red/dynredpar.aspx",
                                         },
                                callback=self.after_search, )]
    def after_search(self,response):
          
        x = HtmlXPathSelector(response)
        
        print x.select('//form[@name="formularioreden"]')