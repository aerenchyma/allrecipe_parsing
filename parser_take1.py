# recipe parser, Take 2

# TODO: indexing by ingredients, searching for "all no milk" or w/e 
# TODO: v/v2/o
# TODO: all formatting questions (bolding ingredients in final print? TeX?)
# TODO: 

###

import lxml.html as lh
import urllib2
from bs4 import BeautifulSoup


def word_sans_comma(w):
	w = w.replace(",","") # because replacing is destructive and need a non-destructive fxn
	w = w.replace(".","")
	return w

#test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
test_recipe = "http://allrecipes.com/recipe/best-chocolate-chip-cookies/"
rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))
ingreds_dict = {}

stopwords = ["in", "on", "the", "of", "what", "and", "&"] # extend / grab from elsewhere??

title = rec_doc.title.string.strip().replace(" - Allrecipes.com","")
srv_num = rec_doc.find(id="lblYield").string

# for each p class=fl-ing
	# class ingredient-amount + class ingredient-name
	# (both of these are with in the p)

test_ingr = rec_doc.findAll("p", {"class" : "fl-ing"}) 

for grp in test_ingr:
	if grp.find(id="lblIngAmount") is not None and grp.find(id="lblIngName") is not None:
		#print "%s %s" % (grp.find(id="lblIngAmount").string, grp.find(id="lblIngName").string)
		amt, nm = (grp.find(id="lblIngAmount").string, grp.find(id="lblIngName").string)
		amount_ingredient = "%s %s" % (amt, nm)
		ingreds_dict[nm] = amt # need to keep track of ingredient names in list or dict so can put them into instructions
		# with a hash of all ingredients, could send these to a (nosql db???) and index for which recipes have which

# directions = rec_doc.find(id="msgDirections")
# print directions.findAll("span", "plaincharacterwrap break")

directions = rec_doc.find("div", "directions")
#print directions
alldirs = " ".join([x.string for x in directions.findAll("span", "plaincharacterwrap break")])

place = 0

replaced = []
for w in [word_sans_comma(x) for x in alldirs.split() if x != "" and x != " " and "ed" not in x[-3:]]:
	for ig_wlst in [y.split() for y in ingreds_dict]:
		if w in ig_wlst and w not in replaced:
			#if ig_wlst[ig_wlst.index(w)-1][-2:] != "ly":
			#print ig_wlst[ig_wlst.index(w)-1]
			alldirs = alldirs.replace(w, ingreds_dict[" ".join(ig_wlst)] + " " + " ".join(ig_wlst))
			place = alldirs.find(w,place) + len(" ".join(ig_wlst))# plus some amount...?? 
			
			replaced += ig_wlst #hmm




ct = 0
al = [x.encode('utf-8') for x in  alldirs.split()]
for item in al[:-1]:
	if word_sans_comma(al[al.index(item)+1]) == word_sans_comma(item):
		print item
		print al[al.index(item)]
		del al[al.index(item)]
alldirs = " ".join(al)





#### TESTING

print title
for k in ingreds_dict:
	print ingreds_dict[k], k

print alldirs








