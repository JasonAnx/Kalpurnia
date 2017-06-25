# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
# import pymongo
from Kalpurnia.items import Url, Posting
from scrapy.exceptions import CloseSpider
from scrapy.conf import settings # settings.py, to access database config variables
from scrapy.exceptions import DropItem


class KalpurniaPipeline(object):
    
    def __init__(self):
        # connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = connection[settings['MONGODB_DB']]
        # self.urlsDB = db[settings['MONGODB_COLLECTION_URLS']]
        # self.ptgsDB = db[settings['MONGODB_COLLECTION_PTGS']]
        # print("\nDatabases Up and Running")
        pass
        
        # for x in self.collection.find():
        #     print( x['url'] )

    def open_spider(self, spider):
        # self.file = open('items.jl', 'wb')
        print("\nThe Spider has Started Crawling")

    def close_spider(self, spider):
        print("\nThe Spider has been killed")
        # self.file.close()

    limit   = 60
    current = 0
    def process_item(self, item, spider):
        if isinstance(item, Url):
            if self.current >= self.limit:
                print("limit reached")
                # raise CloseSpider(spider) 
            # line = json.dumps(dict(item)) + "\n"
            # self.file.write(line)
            self.current += 1

            if self.urlsDB.find_one(item['url']):
                print(item, 'dropped')
                raise DropItem("\n\n\n\nDuplicate item found: %s" % item)
            valid = True
            for data in item:
                if not data:
                    valid = False
                    print(item, 'Missing data')
                    raise DropItem("Missing {0}!".format(data))
            if valid:
                self.urlsDB.insert({item['key']:item['url']})
                # log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
            return item
        # if isinstance(item, Posting):
            # self.ptgsDB.update(dict(item))
                
            