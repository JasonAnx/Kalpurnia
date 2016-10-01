from urllib2 import urlopen
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class QuotesSpider(scrapy.Spider):
    name = "CalpurniaCrawler"
    
    start_urls = [
        'https://en.wikipedia.org/wiki/Calpurnia_(wife_of_Caesar)',
    ]

    def parse(self, response):
        content = response.css('#content')
        
        yield {
            'content':content.css('p *::text').re(r'\w+')
        }
        
        yield {
            'hrefs':content.css('a[href]::text')
        }
        
        yield {
            'content':response.css('a').xpath('@href').extract()
        }
        
        body = '<html><body><span>good</span></body></html>'
        response = HtmlResponse(url='https://en.wikipedia.org/wiki/Calpurnia_(wife_of_Caesar)', body=body)
        d = Selector(response=response).xpath('//span/text()').extract()
        
        print (d) 
        
        for cnt in content.css('div'):
            yield {
                # p parrafo, y todo lo que tenga dentro
                
                #'content': quote.css('ul *::text').re(r'\w+'),
            }
    
    
