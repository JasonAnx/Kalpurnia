from scrapy.spiders import BaseSpider
from urllib2 import urlopen
import scrapy
import Queue
from scrapy import Request
import os # clear console, delete/open files 
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from stemming.porter2 import stem
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
import time # sleep ( n secons )
import json

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

class CalpurniaSpider(scrapy.Spider):
    name = "CalpurniaCrawler"
    allowed_domains = ["wiki.archlinux.org"]


    
    URLsDiccc = {}
    indexId = 1

    DEFAULT_REQUEST_HEADERS = {
       'Accept': 'text/html',
       'Accept-Language': 'en'
    }

    termDiccc = {}

    #os.remove("*.json")
    #print("File Removed!")s

    start_urls = [
        'https://wiki.archlinux.org/',
    ]

    def __init__(self, **kw):
        print("INICIO")
        filelist = [ f for f in os.listdir(".") if f.endswith(".json") ]
        for f in filelist:
            os.remove(f)
        os.system('cls' if os.name == 'nt' else 'clear')
        # dispatcher.connect(self.SpiderKilled, signals.spider_closed)
        print("Staring in 3 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Staring in 2 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Staring in 1 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        return
        
    def parse(self, response):
        print("Started parding " + response.url )
        if not response.url in self.URLsDiccc.keys():        
            self.URLsDiccc[ response.url ] = self.indexId
            self.indexId +=  1
            content = response.css('#content')

            for word in content.css('p *::text').re(r'\w+'):
                stemmedword = stem(word) #aplica stemming a cada palabra
                # si la palabra no existe en el diciconario de postings, 
                # la agrega, y la empareja con un set vacio
                if stemmedword not in self.termDiccc:
                    self.termDiccc[stemmedword] = set()
                # este o no en el diccionario, si la encontro, tiene que agregarla a
                # la lista de postings. Asociada al documento.  
                self.termDiccc[stemmedword].add(self.indexId-1)
                yield {
                    response.url: stemmedword
                }

        hrefs = response.css('a').xpath('@href').extract()
        for ref in hrefs:
            if ref.startswith( "https://wiki.archlinux") or ref.startswith( "http://wiki.archlinux"):
                if ref in self.URLsDiccc.keys():
                    print("\nomiting already parsed page from hrefs found")
                else:
                    print( "\n\n next page: " + ref  + "\n\n" )
                    yield Request(ref, callback=self.parse)
            elif ref.startswith( "/" ):
                URL = response.url
                if URL.endswith("\\"):
                    URL = URL[:-1]
                print("\nlocal path found: " + URL + ref )
                #yield Request( URL + ref, callback=self.parse)
            else:
                print( "\ndroped url " + ref)
        #imprime el diccionario palabra - set ------> postings
        #print self.termDiccc

    def closed(self, reason):
        # print self.termDiccc
        with open('postings.json', 'wb') as fp:
            json.dump(self.termDiccc,fp, sort_keys=True, default=set_default) #indent = 4
        with open('urls.json', 'wb') as fp:
            json.dump(self.URLsDiccc,fp, indent = 4) 
        # with open('postings.json') as data_file:    
        #     data = json.load(data_file)
        # print data

    # def SpiderKilled(self, spider):
    #   # second param is instance of spder about to be closed.
    #   print("\n\n la wea finalizada !!!!!!\n\n")