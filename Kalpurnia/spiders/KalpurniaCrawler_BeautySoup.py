# KALPURNIA
from scrapy.spiders import BaseSpider
from urllib.request import urlopen
from urllib.parse import unquote
from urllib.parse import urlparse
from math import log10
from scrapy import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from Kalpurnia.stemming.porter2 import stem
from Kalpurnia.items import Url, Posting
from scrapy.linkextractors import LinkExtractor  #self.link_extractor = LinkExtractor()
import scrapy.exceptions
import scrapy
import os  # clear console, delete/open files
import time  # sleep ( n secons )
import json
from bs4 import BeautifulSoup
from langdetect import detect  # used to detect the page language
import re



# from urlparse import urlparse # python2
# from collections import namedtuple
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


#import re
#pattern = re.compile("^([A-Z][0-9]+)*$")
#pattern.match(string)


class KalpurniaEmotionSpider(scrapy.Spider):

    name = "KalpurniaCrawler_BeautySoup"

    allowed_domains = ["localhost"]

    URLsDiccc = {}
    sentcsDiccc = {}
    URL_Id = 1
    termDiccc = {}

    # DicccEntry = namedtuple('DicccEntry', 'termFrec pList')

    start_urls = ['http://localhost/', ]

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

    limit = 20
    current = 0

    def parse(self, response):

        # extract all the links from the document
        links = self.link_extractor.extract_links(response)
        # add them to the list of requests (if they are not alreay there)
        for x in links:
            url = unquote(x.url)
            url = url.split('&', 1)[0]
            if not url in self.URLsDiccc.values():
                yield Request(url, callback=self.parse)

        # get the html from the body
        docText = BeautifulSoup(response.body, 'html.parser')
        # kill all script and style elements
        # some pages insert their text using scripts, 
        # so it is not the best approach to remove them, 
        # but for now, we will
        for script in docText(["style", "script"]):
            script.extract()  # rip it out
        # extract the text from the body html
        docText = docText.get_text()

        language = detect(docText)
        if language != 'en':
            print("\nIgnored document %s\n. Detected lang %s" %
                  (response.url, language))
            return

        # tokenize by sentences

        #print (self.sentcsDiccc[self.URL_Id],self.URL_Id)
        # ss = self.sid.polarity_scores(docText)
        # for k in sorted(ss):
        #     print('{0}: {1}, '.format(k, ss[k]), end='')
        # print()

        # assign an ID to the url
        # ... = unquote( ... ).encode('utf8')  # it seems python 3 alreay saves to utf8
        self.URLsDiccc[self.URL_Id] = { 'url': unquote(response.url), 'title': response.css('title::text').extract_first()  } #.encode('utf8') 
        self.URL_Id += 1

        # content = response.css('#content')

        # taken from 
        # http://stackoverflow.com/questions/6181763/converting-a-string-to-a-list-of-words
        # converts the body of the document to a list of words
        wordList = re.sub("[^\w]", " ", docText).split()
        # print (wordList)
        # print ( content.css('p *::text').extract() )


        # self.ALLsDiccc[response.url] = response.css('#content *::text').extract()
        # for word in content.css('p *::text').re(r'\w+'):
        for word in wordList:
            # self.ALLsDiccc[response.url] = 

            # --- No Stemming nor lowercase
            #stemmedword = word.encode('utf8')
            # --- Stemming & lowercase
            stemmedword = stem(word.lower())  #.encode('utf8')

            # if the word is not in the postings dictionary,
            # add it and match it with an empty set  
            if stemmedword not in self.termDiccc:
                self.termDiccc[stemmedword] = {}
            # if the actual url / index id  is not in the   
            # stemmedword associated dict, add it and set 
            # the term frecuency to 1
            # (the number of times that 'stemmedword' occurs in 'URL_Id-1') 
            if (self.URL_Id - 1) not in self.termDiccc[stemmedword]:
                self.termDiccc[stemmedword][self.URL_Id - 1] = 1
            else:
                # increment the term frecuency
                self.termDiccc[stemmedword][self.URL_Id - 1] += 1

    postingsWgts = {}

    def closed(self, reason):
        # Save Results
        with open('urls.json', 'w') as fp:
            json.dump(self.URLsDiccc, fp, indent=4)
        with open('sentences.json', 'w') as fp:
            json.dump(self.sentcsDiccc, fp, indent=4)
        with open('postings.json', 'w') as fp:
            json.dump(self.termDiccc, fp)  # default=set_default, #indent = 4

        # with open('TEST.json', 'w') as fp:
        #     json.dump(self.ALLsDiccc,fp, indent = 4)  

        N = len(self.URLsDiccc)
        for ptng in self.termDiccc:
            self.postingsWgts[ptng] = {}
            # Storing DF in the list of URLs might be impractical
            # self.postingsWgts[ptng]['DF'] = len(self.termDiccc[ptng])
            DF = len(self.termDiccc[ptng])
            for urlId in self.termDiccc[ptng]:
                wtd = 1 + log10(self.termDiccc[ptng][urlId])
                # we choose to store the df in every term url
                self.postingsWgts[ptng][urlId] = {
                    'df': DF,
                    'count': self.termDiccc[ptng][urlId],
                    'weight': wtd,
                    'idf': log10(N / DF)
                }

        with open('postingsWgts.json', 'w') as fp:
            json.dump(self.postingsWgts, fp)

        print("\n\nFinal Results: ")
        print("\n\tPostings dicc size: %d" % len(self.termDiccc))
        print("\n\tURLs dicc size: %d" % len(self.URLsDiccc))
        print("\n")

        # with open('postings.json') as data_file:    
        #     data = json.load(data_file)
        # print data

    # def SpiderKilled(self, spider):
    #   # second param is instance of spder about to be closed.
    #   print("\n\n la wea finalizada !!!!!!\n\n")
