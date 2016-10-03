from scrapy.spiders import BaseSpider
from urllib2 import urlopen
import scrapy
import Queue
from scrapy import Request
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from stemming.porter2 import stem


class CalpurniaSpider(scrapy.Spider):
    name = "CalpurniaCrawler"
    allowed_domains = ["wiki.archlinux.org"]
    start_urls = ['https://wiki.archlinux.org/']

    
    URLsDiccc = {}
    indexId = 1

    DEFAULT_REQUEST_HEADERS = {
       'Accept': 'text/html',
       'Accept-Language': 'en'
    }

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
        return
        
    def parse(self, response):
        if not response.url in self.URLsDiccc.keys():        
            self.URLsDiccc[ response.url ] = self.indexId
            self.indexId = self.indexId + 1
            content = response.css('#content')
            for word in content.css('p *::text').re(r'\w+'):
                yield {
                    response.url: stem( word )
                } 

        hrefs = response.css('a').xpath('@href').extract()

        for ref in hrefs:
            if not ref.startswith( "https://wiki.archlinux.org/"):
                print( "\ndroped url " + ref + "\n")
            else:
                if ref in self.URLsDiccc.keys():
                    print("omiting already parsed page from hrefs found")
                else:
                    print( "\n\n next page: " + ref  + "\n\n" )
                    yield Request(ref, callback=self.parse)

    
    
      
    