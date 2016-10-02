from scrapy.spider import BaseSpider
from urllib2 import urlopen
import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from stemming.porter2 import stem


class QuotesSpider(scrapy.Spider):
    name = "CalpurniaCrawler"
    allowed_domains = ["wiki.archlinux.org"]
    start_urls = ['https://wiki.archlinux.org/']
    
    
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
        yield scrapy.Request(next_page, callback = self.tokenizeDoc)


        #next_page = response.css('li.next a::attr(href)').extract_first()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback = self.parse)
        return

    def tokenizeDoc (self, response):
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
