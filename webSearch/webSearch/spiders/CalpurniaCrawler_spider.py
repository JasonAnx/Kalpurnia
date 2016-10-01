import scrapy


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
        
        for caca in content.css('div'):
            yield {
                # p parrafo, y todo lo que tenga dentro
                
                #'content': quote.css('ul *::text').re(r'\w+'),
            }
