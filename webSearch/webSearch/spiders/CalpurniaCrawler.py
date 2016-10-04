from scrapy.spiders import BaseSpider
from urllib2 import urlopen
from urlparse import urlparse
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


#import re
#pattern = re.compile("^([A-Z][0-9]+)*$")
#pattern.match(string)


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

    start_urls = [
        'https://wiki.archlinux.org/',
    ]

    def __init__(self, **kw):
        print("INICIO")
        #filelist = [ f for f in os.listdir(".") if f.endswith(".json") ]
        #for f in filelist: 
        #    os.remove(f)
        # dispatcher.connect(self.SpiderKilled, signals.spider_closed)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting in 4 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting in 3 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting in 2 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting in 1 seconds")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Parsing")
        return
        
    def parse(self, response):
        #print("Started parsing " + response.url )
        if not response.url in self.URLsDiccc.values():        
            self.URLsDiccc[ self.indexId  ] = response.url
            self.indexId +=  1
            content = response.css('#content')

            for word in content.css('p *::text').re(r'\w+'):
                #aplica stemming a cada palabra
                stemmedword = word                  # Sin Stemming ni lowercase
                #stemmedword = stem( word.lower() )  # Sin Stemming ni lowercase

                # si la palabra no existe en el diciconario de postings, 
                # la agrega, y la empareja con un set vacio
                if stemmedword not in self.termDiccc:
                    self.termDiccc[stemmedword] = set()
                # este o no en el diccionario, si la encontro, tiene que agregarla a
                # la lista de postings. Asociada al documento.  
                self.termDiccc[stemmedword].add(self.indexId-1)
                #yield {
                #    response.url: stemmedword
                #}

        hrefs = response.css('a').xpath('@href').extract()
        for ref in hrefs:
            if ref.startswith( "https://") or ref.startswith( "http://"):
                if not ref in self.URLsDiccc.values():
                    yield Request(ref, callback=self.parse)
            elif ref.startswith( "/" ): # --> its a relative path ------
                # if we're actually in ..org/KDEPLASMA and foud a relative
                # path /PACMAN, we must go to ..org/PACMAN, not to 
                # ..org/KDEPLASMA/PACMAN, so we can't just append new refs  
                parsed_uri = urlparse(response.url)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                # -------------------------------------------------------
                if domain.endswith("/"):
                    domain = domain[:-1]
                next_page = domain + ref
                #print("\nrelative path found: " + next_page )
                yield Request( next_page, callback=self.parse)
            #else:
                #print( "\ndroped url " + ref)

        #imprime el diccionario palabra - set ------> postings
        #print self.termDiccc

    def closed(self, reason):
        # print self.termDiccc
        with open('postingsSinStemm.json', 'wb') as fp:
            json.dump(self.termDiccc,fp, sort_keys=True, default=set_default, indent = 4) #indent = 4
        with open('urlsSinStemm.json', 'wb') as fp:
            json.dump(self.URLsDiccc,fp, indent = 4) 
        
        print ( "\n\nFinal Results: " )
        print ( "\n\tPostings dicc size: %d" % len( self.termDiccc ) )
        print ( "\n\tURLs dicc size: %d" % len( self.URLsDiccc ) )
        print ( "\n")
         
        # with open('postings.json') as data_file:    
        #     data = json.load(data_file)
        # print data

    # def SpiderKilled(self, spider):
    #   # second param is instance of spder about to be closed.
    #   print("\n\n la wea finalizada !!!!!!\n\n")