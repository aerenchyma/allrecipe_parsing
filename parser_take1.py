# recipe parser, Take 2

import lxml.html as lh
import urllib2
from bs4 import BeautifulSoup


test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))
ingreds_dict = {}

title = rec_doc.title.string.strip().replace(" - Allrecipes.com","")
srv_num = rec_doc.find(id="lblYield").string

# for each p class=fl-ing
	# class ingredient-amount + class ingredient-name
	# (both of these are with in the p)

test_ingr = rec_doc.findAll("p", {"class" : "fl-ing"}) # this is only finding the first ingredient, select for others

# print test_ingr[3]

for grp in test_ingr:
	if grp.find(id="lblIngAmount") is not None and grp.find(id="lblIngName") is not None:
		#print "%s %s" % (grp.find(id="lblIngAmount").string, grp.find(id="lblIngName").string)
		amt, nm = (grp.find(id="lblIngAmount").string, grp.find(id="lblIngName").string)
		amount_ingredient = "%s %s" % (amt, nm)
		ingreds_dict[nm] = amt # need to keep track of ingredient names in list or dict so can put them into instructions





#### TESTING

print title
print srv_num
#print " ".join([y for y in [str(x.string) for x in test_ingr] if y != ''])
# above: should be in-fxn, and will want to bold ingredients perhaps? formatting q TODO
#print test_ingr







