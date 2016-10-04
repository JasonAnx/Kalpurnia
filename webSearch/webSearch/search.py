import json
import sys, getopt
import numpy as np
from spiders.stemming.porter2 import stem


json_postings = open('postingsSinStemm.json')
json_urls     = open('urlsSinStemm.json')

postings = json.load( json_postings )
urls     = json.load( json_urls     )


print("\n\n")

#opts, args = getopt.getopt(sys.argv,"hi:o:",["ifile=","ofile="])
#
#input
#for opt, arg in opts:
#    if opts in ("-i"):
#        input = args    
#        print (input)
#


sa = 'KDE'
sb = 'plasma'
sc = 'desktop'

print("resultados de la busqueda %s %s % s:\n" % (sa, sb, sc) )

stem = False

if stem:
    sa = stem( sa.lower() ) #aplica stemming a cada palabra
    sb = stem( sb.lower() ) #aplica stemming a cada palabra
    sc = stem( sc.lower() ) #aplica stemming a cada palabra

a = postings[ sa ]
b = postings[ sb ]
c = postings[ sc ]

d = [a, b, c]

result = set(d[0]).intersection(*d)

for res in result: # res entera
    print( urls[ str(res) ] )

#print ( set(a) )

#print ( list( set(a) & set(b)) )

print("\n\n")

json_postings.close()
json_urls.close()