import json
import numpy as np

json_postings = open('spiders/postings.json')
json_urls     = open('spiders/urls.json')

postings = json.load( json_postings )
urls     = json.load( json_urls     )

#print ( postings['Arch'] )
#print ( '\n' ) 
#print ( postings['wiki'] )
#print ( '\n' ) 

a = postings['Arch']
b = postings['KDE']
c = postings['linux']

d = [a, b, c]

result = set(d[0]).intersection(*d)

for res in result: # res entera
    print( urls[ str(res) ] )

#print ( set(a) )

#print ( list( set(a) & set(b)) )


json_postings.close()