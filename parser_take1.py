# recipe parser, Take 2

import lxml.html as lh
import urllib2
from bs4 import BeautifulSoup


test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))

title = rec_doc.title.string.strip().replace(" - Allrecipes.com","")

srv_num = rec_doc.find(id="lblYield").string

# for each p class=fl-ing
	# class ingredient-amount + class ingredient-name
	# (both of these are with in the p)

test_ingr = rec_doc.find("p", {"class" : "fl-ing"}) # this is only finding the first ingredient, select for others



#### testing

print title
print srv_num
print [str(x.string.strip()) for x in test_ingr if x != '']




