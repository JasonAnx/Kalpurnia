# Install aspell

http://stackoverflow.com/questions/1957808/how-can-i-install-pspell-in-php5-ubuntu

    sudo apt-get update  # without this, c9 will give `unable to locate package`
    sudo apt-get install libpspell-dev 
    sudo apt-get install php5-pspell
    sudo apt-get install aspell-en
    
if you want to use other languajes, spanish for example:
    sudo apt-get install aspell-es
    
Then, restart the server:
    sudo service apache2 restart 
    
    