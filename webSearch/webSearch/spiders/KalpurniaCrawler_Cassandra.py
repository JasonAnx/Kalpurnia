# KALPURNIA
from scrapy.spiders import BaseSpider
from urllib.request import urlopen
from urllib.parse import unquote
from urllib.parse import urlparse
from math import log10
from scrapy import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from ..stemming.porter2 import stem
from webSearch.items import Url, Posting
from scrapy.linkextractors import LinkExtractor  #self.link_extractor = LinkExtractor()
import scrapy.exceptions
import scrapy
import os  # sys-independent clear console, delete/open files
import time  # sleep ( n secons )
import hashlib
import json
# Cassandra ========================
from cassandra.cluster import Cluster
from cassandra import DriverException


from bs4 import BeautifulSoup
from langdetect import detect  # used to detect the page language
# # from nltk import tokenize
# from nltk import tokenize
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

    name = "KalpurniaCrawler_Cassandra"

    allowed_domains = ["www.nacion.com"]

    URLsDiccc = {}
    sentcsDiccc = {}
    # URL_Id = 1
    termDiccc = {} # entire collection terms

    # DicccEntry = namedtuple('DicccEntry', 'termFrec pList')

    start_urls = ['http://www.nacion.com', ]

    def __init__(self, **kw):
        print("Spider running")
        #filelist = [ f for f in os.listdir(".") if f.endswith(".json") ]
        #for f in filelist: 
        #    os.remove(f)
        # dispatcher.connect(self.SpiderKilled, signals.spider_closed)
        self.link_extractor = LinkExtractor()
        self.cluster = Cluster(['127.0.0.1'])
        self.session = self.cluster.connect('test')

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
            if not url in self.URLsDiccc.keys():
                yield Request(url, callback=self.parse)
            else:
                print("url has already been parsed", url)

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
        if language != 'es':
            print("\nIgnored document %s\n. Detected lang %s" %
                  (response.url, language))
            return

        # assign an ID to the url
        # ... = unquote( ... ).encode('utf8')  # it seems python 3 alreay saves to utf8
        docURL = unquote(response.url) 
        docID = hashlib.sha256(docURL.encode()).hexdigest()
        docTitle = response.css('title::text').extract_first().replace("'", "''") # escape single quotes. Needed for INSERT
        tupla = { "docid": (docID), "docurl": docURL, "title":  docTitle} 
        self.URLsDiccc[docURL] = 1

        try:
            query = "INSERT INTO test.urls JSON  '{}';".format( json.dumps( tupla ) )
            self.session.execute(query)
        except Exception as excp:
            print("=======================")
            print(query)
            print(excp)

        # content = response.css('#content')

        # taken from 
        # http://stackoverflow.com/questions/6181763/converting-a-string-to-a-list-of-words
        # converts the body of the document into a list of words
        wordList = re.sub("[^\w]", " ", docText).split()

        docterms = {}

        for word in wordList:
            # self.ALLsDiccc[response.url] = 

            # --- No Stemming 
            stemmedword = word.lower()
            # --- Stemming & lowercase
            # stemmedword = stem(word.lower())  #.encode('utf8')

            # if the word is not in the postings dictionary,
            # add it and match it with an empty set  
            if stemmedword not in self.termDiccc:
                self.termDiccc[stemmedword] = {}
            if stemmedword not in docterms:
                docterms[stemmedword] = 1
            else:
                docterms[stemmedword] += 1
            # if the actual url / index id  is not in the   
            # stemmedword associated dict, add it and set 
            # the term frecuency to 1
            # (the number of times that 'stemmedword' occurs in 'URL_Id-1') 
            if (docID) not in self.termDiccc[stemmedword]:
                self.termDiccc[stemmedword][docID] = 1
            else:
                # increment the term frecuency
                self.termDiccc[stemmedword][docID] += 1
        # --------------------------
        try:
            tupla = {"docid":docID, "palabras":docterms}
            query = " INSERT INTO frecpalabras JSON '{}';".format( json.dumps( tupla ) )
            self.session.execute(query)
        except Exception as excp:
            print("=======================")
            print(query)
            print(excp)
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

        # To ensure all connections are properly closed, you should always call shutdown() on a Cluster instance when you are done with it.
        self.session.shutdown()

        # with open('postings.json') as data_file:    
        #     data = json.load(data_file)
        # print data

    # def SpiderKilled(self, spider):
    #   # second param is instance of spder about to be closed.
    #   print("\n\n la wea finalizada !!!!!!\n\n")
