## Mongo (Debian Based)
Install mongodb

    sudo apt install mongodb



### Mongo (Arch)
~~By default, the spider stores its results in a .json, there's no need to add `-o name.json`, just run~~
Using .json to store the data has become inefficient, now we're using pymongo.
On Arch Linux, copy and paste into your terminal the following command:

    sudo pacman -S mongodb  \
    boost-libs libsasl openssl pcre snappy wiredtiger yaml-cpp --needed #dependecies

and then enable the service: `systemctl [start/enable] mongodb.service`

To connect to mongo from python, install `python-pymongo`

    sudo pacman -S python-pymongo --needed

### Robomongo
pacaur -S robomongo

**Note:** although robomongo's size is just 18.20 mb, there's an issue with the source, and its size is about ~160mb. 

After the database has been created, expand it and right click on 'collections' > 'create collections'
# todo 
