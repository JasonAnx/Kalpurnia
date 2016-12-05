---
# Scrapy-based Web Crawler and Search Engine
### University of Costa Rica
#### CI-2414 Information Retrieval
---

### Update dec 4 2016

#### Added a Sentiment analysis spider

In order to use the new spider, you will also need to install [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and NLTK. [langdetect](https://pypi.python.org/pypi/langdetect) 

    sudo pip3 install beautifulsoup4 
    sudo pip3 install langdetect
    sudo pip3 install nltk
    
Antes de ejecutar el programa se debe descargar el dataset de reviews de películas:
    
    $ python3
    >>> import nltk
    >>> nltk.download()
    >>> d
    >>> movie_reviews
    >>> q


# Installation

## Debian-based OS
Install Kalpurnia dependencies and Apache

    sudo apt -y install  apache2 php libapache2-mod-php aspell-en php-pspell
And restart apache 

    systemctl restart apache2

After installing apache, clone this repository into `/var/www/html/`

install mongodb

    sudo apt install mongodb
 
and then, use pip to install Scrapy
 
    sudo apt install python3-pip
    sudo apt install libssl-dev
    sudo pip3 install --upgrade pip # else, scrapy will fail to install
    sudo pip3 install scrapy
    sudo pip3 install pymongo
    sudo pip3 install langdetect




## Install (Arch Linux) 
### Update 
> As of November 2016, the scrapy version on the Arch Linux repositories is 1.0.5 so **don't install from pacman**.
Last Scrapy version [11-2016] is 1.2.1.
Version 1.0.5 does not contain some exceptions signals used by Kalpurnia.

Instead of using pacman, install Scrapy using python-pip:

    sudo pacman -Syy python2-pip python-pip
    
**DO NOT UPGRADE PIP to version 9**
If you istalled scrapy from pacman, unistall it. Then install scrapy:

    sudo pip install Scrapy

The following packages installed by scrapy for Arch Linux are no longer needed and can be uninstalled.

    python2-appdirs python2-attrs python2-crypto python2-cryptography python2-cssselect python2-enum34 python2-idna python2-ipaddress python2-lxml python2-packaging python2-pyasn1 python2-pyasn1-modules python2-pyopenssl python2-pyparsing python2-queuelib python2-service-identity python2-setuptools python2-twisted python2-w3lib python2-zope-interface

# Usage
Run the spider on `/webSearch/webSearch/spiders` with

    scrapy crawl kalpurniaCrawler --nolog
`--nolog` deactivates the scrapy log during runtime 

By default, `kalpurniaCrawler` stores its results in a .json, so there's no need to add `-o name.json`.

#### memurandum
This is extremely useful https://rtyley.github.io/bfg-repo-cleaner/
