# Usage

## Cloud 9

http://stackoverflow.com/questions/1957808/how-can-i-install-pspell-in-php5-ubuntu

    sudo apt-get update  # without this, c9 will give `unable to locate package`
    sudo apt-get install libpspell-dev 
    sudo apt-get install php5-pspell
    sudo apt-get install aspell-en
    
if you want to use other languajes, spanish for example:
    sudo apt-get install aspell-es
    
Then, restart the server:
    sudo service apache2 restart 
    
## Arch Linx

required
    sudo pacman -S apache php-pspell php-apache  --needed
Then, follow this instructions https://wiki.archlinux.org/index.php/Apache_HTTP_Server#PHP

After that, restart apache:
    systemctl start httpd.service
