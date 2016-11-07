# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Url(scrapy.Item):
    # define the fields for your item here like:
    key = scrapy.Field()
    url = scrapy.Field()
    pass

class Posting(scrapy.Item):
    # define the fields for your item here like:
    posting = scrapy.Field()
    url_id = scrapy.Field()
    pass