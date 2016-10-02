from scrapy.spiders import BaseSpider
from urllib2 import urlopen
import scrapy
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

    #os.remove("*.json")
    #print("File Removed!")s

    start_urls = [
        'https://wiki.archlinux.org/',
    ]

    def __init__(self, **kw):
        print("sadfasdf")
        return
    
    
        
    def parse(self, response):
        
        #yield {
        #    'content':response.css('a').xpath('@href').extract()
        #}

        #yield {
        #        'url': response.url
        #    };
#
#
#
        #hrefs = response.css('a').xpath('@href').extract()
        #for ref in hrefs:
        #    yield {
        #        'hrefs': ref 
        #    };
        

        next_page = "https://wiki.archlinux.org/"

        yield Request(next_page, callback = self.getUrls     )

        yield Request(next_page, callback = self.tokenizeDoc )

        

        return

    def tokenizeDoc (self, response):
        print("SUCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCc")
        content = response.css('#content')

        #"https://www.archlinux.org/"

        for word in content.css('p *::text').re(r'\w+'):
            yield {
                'content': stem( word )
            }
        
        #yield {
        #    'hrefs':content.css('a[href]::text')
        #}
        return

    
      
    def getUrls (self, response):

        hrefs = response.css('a').xpath('@href').extract()
        for ref in hrefs:
            self.URLsDiccc[ self.indexId ] = ref
            self.indexId = self.indexId + 1    
            yield {
                'hrefs': ref 
            };
        
        #print( self.URLsDiccc ) 

 

        return
        

