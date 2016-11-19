# Scrapy-based Web Crawler and Search Engine
## CI-2414 Information Retrieval
### University of Costa Rica

# Update
As of November 2016, the scrapy version on the Arch Linux repositories is 1.0.5 so **don't install from pacman**.
Last Scrapy version [11-2016] is 1.2.1. 
Version 1.0.5 does not contain some exceptions signals used by Kalpurnia.
So instead of using pacman, install python-pip and use it to install Scrapy:

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

# apache host and php on debian and derivates  (Ubuntu, Mint ...)

https://www.howtoforge.com/tutorial/install-apache-with-php-and-mysql-on-ubuntu-16-04-lamp/

clone this repository in /var/www/html/

	sudo apt install aspell-en
	sudo apt install php-pspell
	sudo service apache2 restart 


#### memurandum
This is extremely useful https://rtyley.github.io/bfg-repo-cleaner/
