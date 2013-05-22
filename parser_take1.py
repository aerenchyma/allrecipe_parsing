# recipe parser, Take 2

# TODO: indexing by ingredients, searching for "all no milk" or w/e 
# TODO: v/v2/o
# TODO: all formatting questions (bolding ingredients in final print? TeX?)
# TODO: 

###

import lxml.html as lh
import urllib2
from bs4 import BeautifulSoup
import re


def word_sans_comma(w):
	if w[-1] =="," or w[-1] == ".":
		#print "comma repl", w
		w = w.replace(",","") # because replacing is destructive and need a non-destructive fxn
		w = w.replace(".","")
	return w

#test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
test_recipe = "http://allrecipes.com/recipe/best-chocolate-chip-cookies/"
rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))
ingreds_dict = {}

stopwords = ["in", "on", "the", "of", "what", "and", "&", "are", "you", "a", "an", "or", "why"] # extend / grab from elsewhere??
cooking_verbs = ["browned", "softened"] # add more if not get from elsewhere/learning



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
		ingreds_dict[nm.encode('utf-8')] = amt.encode('utf-8') # need to keep track of ingredient names in list or dict so can put them into instructions
		# with a hash of all ingredients, could send these to a (nosql db???) and index for which recipes have which

# directions = rec_doc.find(id="msgDirections")
# print directions.findAll("span", "plaincharacterwrap break")

directions = rec_doc.find("div", "directions")
#print directions
alldirs = " ".join([x.string for x in directions.findAll("span", "plaincharacterwrap break")])

place = 0

print ingreds_dict

debugging = []
replaced = []
for w in [x.encode('utf-8') for x in alldirs.split() if x != "" and x != " " and "ed" not in x[-3:]]:
	print "w is:", w
	#print "adding ed: ", w + "ed" # never get brown here, currently
	for ig_wlst in [y.split() for y in ingreds_dict]:
		#print ig_wlst
		ig_wlst = [x.encode('utf-8') for x in ig_wlst]
		if (word_sans_comma(w) in ig_wlst or w in ig_wlst) and word_sans_comma(w.encode('utf-8')) not in [x.encode('utf-8') for x in replaced]: #and w.encode('utf-8') not in " ".join(ig_wlst): # encoding consistent enough here?
			#print "index",ig_wlst.index(w), w
			#if not 
			#alldirs = alldirs.replace(w, ingreds_dict[" ".join(ig_wlst)] + " " + " ".join(ig_wlst)) # replaces ALL instances of str
			print ingreds_dict[" ".join(ig_wlst)] + " " + " ".join(ig_wlst)
			alldirs = re.sub(re.escape(w) + r"[^a-zA-Z]", " " + ingreds_dict[" ".join(ig_wlst)] + " " + " ".join(ig_wlst) + "  ", alldirs) # note the two spaces at the end to allow for easy dedupe of words
			#print "End of ALLDIRS: ", alldirs[-20:]
			place = alldirs.find(w,place) + len(" ".join(ig_wlst))# plus some amount...?? or not
			
			replaced += [x.encode('utf-8') for x in ig_wlst] #hmm

print replaced


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







