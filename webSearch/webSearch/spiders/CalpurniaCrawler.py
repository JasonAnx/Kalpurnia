from scrapy.spiders import BaseSpider
from urllib2 import urlopen
from urlparse import urlparse
from math import log10
import scrapy
import Queue
from scrapy import Request
from collections import namedtuple
import os # clear console, delete/open files 
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from ..stemming.porter2 import stem
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
    allowed_domains = [
        "wiki.archlinux.org"
    ]


    
    URLsDiccc = {}
    URL_Id = 1

    DEFAULT_REQUEST_HEADERS = {
       'Accept': 'text/html',
       'Accept-Language': 'en'
    }

    # DicccEntry = namedtuple('DicccEntry', 'termFrec pList')

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

        # print("Starting in 4 seconds")
        # time.sleep(1)
        # os.system('cls' if os.name == 'nt' else 'clear')

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
        # ---------- 
        if response.url in self.URLsDiccc.values():
            return
        
        self.URLsDiccc[ self.URL_Id  ] = response.url.encode('utf8')
        self.URL_Id +=  1
        content = response.css('#content')
        
        # self.ALLsDiccc[response.url] = response.css('#content *::text').extract()
        # print( content.css('p *::text').extract() )
        for word in content.css('p *::text').re(r'\w+'):
            # self.ALLsDiccc[response.url] = 
            # No Stemming nor lowercase
            #stemmedword = word.encode('utf8')
            
            # Stemming & lowercase
            stemmedword = stem( word.lower() ).encode('utf8')
            # if the word is not in the postings dictionary,
            # add it and match it with an empty set  
            if stemmedword not in self.termDiccc:
                self.termDiccc[stemmedword] = {}
            # if the actual url / index id  is not in the   
            # stemmedword associated dict, add it and set 
            # the term frecuency to 1
            # (the number of times that 'stemmedword' occurs in 'URL_Id-1') 
            if (self.URL_Id-1) not in self.termDiccc[stemmedword]:
                self.termDiccc[stemmedword][self.URL_Id-1] = 1
            else:
                # increment the term frecuency
                self.termDiccc[stemmedword][self.URL_Id-1] += 1
            # self.termDiccc[stemmedword][0]
        #-for-

        hrefs = response.css('a').xpath('@href').extract()
        for ref in hrefs:
            # remove other arguments
            ref = ref.split('&', 1)[0]

            if ref.startswith( "/" ): # --> its a relative path ------
                # if we're actually on ..org/KDEPLASMA and find a relative
                # path to /PACMAN, we must go to ..org/PACMAN, not to 
                # ..org/KDEPLASMA/PACMAN, so we can't just append new refs  
                parsed_uri = urlparse(response.url)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                # -------------------------------------------------------

                if domain.endswith("/"):
                    # ref[1:] would remove the '/' from ref,
                    # but we can't assume all domains end with '/'
                    domain = domain[:-1]
                
                ref = domain + ref
                #print("\nrelative path found: " + next_page )
                # yield Request( ref, callback=self.parse)
            if ref.startswith( "https://") or ref.startswith( "http://"):
                yield Request(ref, callback=self.parse)
            #else:
                #print( "\ndroped url " + ref)
            
    postingsWgts = {}
    def closed(self, reason):
        # Save Results
        with open('postings.json', 'wb') as fp:
            json.dump(self.termDiccc,fp, default=set_default, indent = 4, ensure_ascii=False) #indent = 4
        with open('urls.json', 'wb') as fp:
            json.dump(self.URLsDiccc,fp, indent = 4, ensure_ascii=False)
        # with open('TEST.json', 'wb') as fp:
        #     json.dump(self.ALLsDiccc,fp, indent = 4)  
        
        N =  len ( self.URLsDiccc )
        for ptng in self.termDiccc:
            self.postingsWgts[ptng] = {}
            # Storing DF in the list of URLs might be impractical
            # self.postingsWgts[ptng]['DF'] = len(self.termDiccc[ptng])
            DF = len(self.termDiccc[ptng])
            for urlId in self.termDiccc[ptng]:
                wtd = 1 + log10( self.termDiccc[ptng][urlId] )
                # we choose to store the df in every term url
                self.postingsWgts[ptng][urlId] = {
                    "df": DF,
                    "count": self.termDiccc[ptng][urlId],
                    "weight":wtd,
                    "idf": log10( N / DF )
                }

        with open('postingsWgts.json', 'wb') as fp:
            json.dump(self.postingsWgts,fp, indent = 4, ensure_ascii=False)
        
        
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