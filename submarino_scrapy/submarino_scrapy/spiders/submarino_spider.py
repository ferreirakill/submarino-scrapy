import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from submarino_scrapy.items import SubmarinoScrapyItem

class SubmarinoSpiderSpider(CrawlSpider):
    name = 'submarino_spider'
    allowed_domains = ['submarinoviagens.com.br']
    start_urls = ['http://www.submarinoviagens.com.br/Passagens/selecionarvoo?SomenteIda=false&Origem=Sao%20Paulo%20-%20Guarulhos%20/%20SP,%20Brasil,%20Cumbica%20--GRU---&Destino=Ibiza,%20Espanha%20--IBZ---&Origem=Ibiza,%20Espanha%20--IBZ---&Destino=Sao%20Paulo%20-%20Guarulhos%20/%20SP,%20Brasil,%20Cumbica%20--GRU---&Data=08/04/2013&Data=18/04/2013&NumADT=1&NumCHD=0&NumINF=0&SomenteDireto=&Hora=&Hora=&selCabin=&Multi=false']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = SubmarinoScrapyItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
