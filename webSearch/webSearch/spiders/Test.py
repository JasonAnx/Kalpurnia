# KALPURNIA
from scrapy.spiders import BaseSpider
from urllib.request import urlopen
from urllib.parse import  unquote
from urllib.parse import  urlparse
from math import log10
from scrapy import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
import json # json dump
import scrapy.exceptions
import scrapy


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


#import re
#pattern = re.compile("^([A-Z][0-9]+)*$")
#pattern.match(string)


class TestSpider(scrapy.Spider):
    
    name = "test"

    allowed_domains = [
        'https://wiki.archlinux.org/'
    ]

    # DicccEntry = namedtuple('DicccEntry', 'termFrec pList')

    start_urls = [
        'https://wiki.archlinux.org/',
    ]
    
    def __init__(self, **kw):
        self.link_extractor = LinkExtractor()

    def parse(self, response):
        # ---------- 
        content = response.css('#content')
        hrefs = response.css('a').xpath('@href').extract()
        i = 1
        urlsN = {}
        for ref in hrefs:
            # remove other arguments
            ref = ref.split('&', 1)[0]
            if ref.startswith( "/" ): # --> its a relative path ------
                # if we're actually on ..org/KDEPLASMA and find a relative
                # path to /PACMAN, we must go to ..org/PACMAN, not to 
                # ..org/KDEPLASMA/PACMAN, so we can't just append new refs  
                parsed_uri = urlparse(response.url)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                # -------------------------------------------------------
                if domain.endswith("/"):
                    # ref[1:] would remove the '/' from ref,
                    # but we can't assume all domains end with '/'
                    domain = domain[:-1]
                  
                ref = domain + ref
                #print("\nrelative path found: " + next_page )
                # yield Request( ref, callback=self.parse)
            if ref.startswith( "https://") or ref.startswith( "http://"):
                url = unquote(ref)
                if not url in urlsN:
                    urlsN[url] = " "
                print (i ,": ", url)
                i = i+1
            
        print('\n\n\n\n\n\n\n\n\n')
        urlsXt = {}
        i = 1
        links = self.link_extractor.extract_links(response)
        for x in links:
            url = unquote( x.url)
            url = url.split('&', 1)[0]
            if not url in urlsXt:
                urlsXt[url] = " "
            print (i ,": ", url )
            i = i+1
        #- save results
        with open('urlsN.json', 'w') as fp:
            json.dump(urlsN,fp, ensure_ascii=False, sort_keys=True, indent = 4)
        with open('urlsXt.json', 'w') as fp:
            json.dump(urlsXt,fp, ensure_ascii=False, sort_keys=True, indent = 4)