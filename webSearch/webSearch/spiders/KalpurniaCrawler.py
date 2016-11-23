# KALPURNIA
from scrapy.spiders import BaseSpider
from urllib.request import urlopen
from urllib.parse import  unquote
from urllib.parse import  urlparse
# from urlparse import urlparse # python2
from math import log10
from scrapy import Request
# from collections import namedtuple
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from ..stemming.porter2 import stem
from webSearch.items import Url, Posting
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
from scrapy.linkextractors import LinkExtractor #self.link_extractor = LinkExtractor()
import scrapy.exceptions
import scrapy
import os # clear console, delete/open files
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
    
    name = "KalpurniaCrawler"

    allowed_domains = [
        "wiki.archlinux.org"
    ]

    URLsDiccc = {}
    URL_Id = 1
    termDiccc = {}

    # DicccEntry = namedtuple('DicccEntry', 'termFrec pList')

    start_urls = [
        'https://wiki.archlinux.org/',
    ]

    def __init__(self, **kw):
        print("Spider running")
        #filelist = [ f for f in os.listdir(".") if f.endswith(".json") ]
        #for f in filelist: 
        #    os.remove(f)
        # dispatcher.connect(self.SpiderKilled, signals.spider_closed)
        self.link_extractor = LinkExtractor()
        
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
    
    limit   = 20
    current = 0
    def parse(self, response):
        
        links = self.link_extractor.extract_links(response)
        for x in links:
            url = unquote( x.url)
            url = url.split('&', 1)[0]
            if not url in self.URLsDiccc.values():
                yield Request( url, callback = self.parse )
        
        # it seems python 3 alreay saves to utf8
        self.URLsDiccc[ self.URL_Id  ] = unquote( response.url )#.encode('utf8')
        self.URL_Id +=  1
        content = response.css('#content')
        
        # self.ALLsDiccc[response.url] = response.css('#content *::text').extract()
        for word in content.css('p *::text').re(r'\w+'):
            # self.ALLsDiccc[response.url] = 
            
            # --- No Stemming nor lowercase
            #stemmedword = word.encode('utf8')
            # --- Stemming & lowercase
            stemmedword = stem( word.lower() )#.encode('utf8')

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


  
    postingsWgts = {}
    def closed(self, reason):
        # Save Results
        with open('postings.json', 'w') as fp:
            json.dump(self.termDiccc,fp, default=set_default, ensure_ascii=False) #indent = 4
        with open('urls.json', 'w') as fp:
            json.dump(self.URLsDiccc,fp, ensure_ascii=False)
        # with open('TEST.json', 'w') as fp:
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
                    'df': DF,
                    'count': self.termDiccc[ptng][urlId],
                    'weight':wtd,
                    'idf': log10( N / DF )
                }

        with open('postingsWgts.json', 'w') as fp:
            json.dump(self.postingsWgts,fp, ensure_ascii=False)
        
        
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