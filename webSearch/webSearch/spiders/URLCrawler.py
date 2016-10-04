from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field


class URL(Item):
    url   = Field()
    title = Field()

# Aranya que consigue todas las urls en un dominio
class URLCrawler(CrawlSpider):
    name = 'URL'
    
    allowed_domains = ["wiki.archlinux.org"]
    start_urls = ['http://wiki.archlinux.org']

    rules = (Rule(SgmlLinkExtractor(), callback='parse_url', follow=True), )

    def parse_url(self, response):
        item = URL()
        item['title'] = response.xpath('//title/text()').extract_first()
        item['url'  ] = response.url
        return item