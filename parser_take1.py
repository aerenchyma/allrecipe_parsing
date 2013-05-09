# recipe parser, Take 2

import lxml.html as lh
import urllib2
from bs4 import BeautifulSoup


test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))

print rec_doc






