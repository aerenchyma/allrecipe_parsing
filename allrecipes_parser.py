# recipe parser
# save in directory for text file recipe; will generate files of parsed recipes 
# (currently in plain text, not formatted TODO)

# TODO: indexing by ingredients
# TODO: all formatting questions/alterations, TeX
# TODO: storage for indexing
# TODO: make less procedural
# TODO: consider parser (diff problems)
# TODO: anywhere esp useful for min ed dist?

###

import urllib2
from bs4 import BeautifulSoup
import re
import sys
import argparse


def word_sans_comma(w):
	if w[-1] =="," or w[-1] == ".":
		w = w.replace(",","") # because strings are immutable + need non-destructive fxn w/ return val
		w = w.replace(".","")
	return w

## recipe url entering options for testing -- note that test_recipe variable has a dependency later on
#test_recipe = sys.argv[1]
#test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
#test_recipe = "http://allrecipes.com/recipe/best-chocolate-chip-cookies/"
# test_recipe = "http://allrecipes.com/Recipe/Chicken-Pot-Pie-IX/"
test_recipe = "http://allrecipes.com/Recipe/Chicken-Teriyaki-with-Asparagus/"

rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))
ingreds_dict = {}

# TODO: get these things in a more sustainable/responsible way (?)
stopwords = ["in", "on", "the", "of", "what", "and", "&", "are", "you", "a", "an", "or", "why"] 
meat_words = ["chicken", "beef", "lamb", "venison", "meat", "turkey", "salami", "bologna", "ham"]
dairy_words = ["cheese", "butter", "milk", "mozzerella", "mozzarella", "cheddar", "monterey jack", "colby", "colby jack", "swiss", "bleu cheese", "whey"] #extend -- coconut milk is a problem in this list
other_nonvegan = ["egg"]
all_nonvegan = meat_words + dairy_words + other_nonvegan

# for category determination later
vegan = True
non_dairy = True
veg = True
omni = True

title = rec_doc.title.string.strip().replace(" - Allrecipes.com","")
srv_num = rec_doc.find(id="lblYield").string
test_ingr = rec_doc.findAll("p", {"class" : "fl-ing"}) 

for grp in test_ingr:
	if grp.find(id="lblIngAmount") is not None and grp.find(id="lblIngName") is not None:
		amt, nm = (grp.find(id="lblIngAmount").string, grp.find(id="lblIngName").string)
		amount_ingredient = "%s %s" % (amt, nm)
		ingreds_dict[nm.encode('utf-8')] = amt.encode('utf-8') # need to keep track of ingredient names for instrs
		# hash |-> db -- a thought..

directions = rec_doc.find("div", "directions")
alldirs = " ".join([x.string for x in directions.findAll("span", "plaincharacterwrap break")])

place = 0

## TODO: if you've replaced WITH the same word twice, stop replacing it -- it's usually not harmful aside from other problems, but it's silly

# keep track of words that have been replaced to avoid doubling
replaced = []
new_dirs_lines = []
punct_add = " "
for w in [x.encode('utf-8') for x in alldirs.split() if x != "" and x != " " and "ed" not in x[-3:] and x not in stopwords]:
	#control stmts for category determination
	if word_sans_comma(w) in meat_words or word_sans_comma(w)+"s" in meat_words:
		vegan = False
		veg = False
	elif word_sans_comma(w) in dairy_words or word_sans_comma(w)+"s" in dairy_words:
		vegan = False
		non_dairy = False
	elif word_sans_comma(w) in other_nonvegan or word_sans_comma(w)+"s" in other_nonvegan:
		vegan = False

	for ig_wlst in [y.split() for y in ingreds_dict]:
		ig_wlst = [x.encode('utf-8') for x in ig_wlst]
		if (word_sans_comma(w) in ig_wlst or w in ig_wlst) and word_sans_comma(w.encode('utf-8')) not in [x.encode('utf-8') for x in replaced] and w.encode('utf-8') not in [x.encode('utf-8') for x in replaced]: #and w.encode('utf-8') not in " ".join(ig_wlst): # TODO improve consistency of encoding
			subst_str = ingreds_dict[" ".join(ig_wlst)] + " " + " ".join(ig_wlst) + " " # note spacing changes -- TODO make neater/clearer what's going on
			if w[-1] == ".":
				punct_add = ". "
			elif w[-1] == ",":
				punct_add = ", "
			alldirs = re.sub(re.escape(w) + r"[^a-zA-Z]", " " + " " + subst_str + " " if w[-1].isalnum() and punct_add != "" else subst_str.rstrip() + punct_add, alldirs) # assume if isalnum, no punct_add -- safe?
			place = alldirs.find(w,place) + len(" ".join(ig_wlst)) # correct amt but not needed

			replaced += [x.encode('utf-8') for x in ig_wlst] 


ct = 0
al = [x.encode('utf-8') for x in  alldirs.split()]
for item in al[:-1]:
	if word_sans_comma(al[al.index(item)+1]) == word_sans_comma(item):
		del al[al.index(item)]
alldirs = " ".join(al) 

## collect necessary information

recipe_title = title
ingredient_strs = ["%s %s" % (ingreds_dict[k], k) for k in ingreds_dict.keys()]
directions_str = alldirs
file_title = "_".join(recipe_title.split()) + ".txt"

# category & dairy status determination
category = "uncategorized" # just in case
dairy = "incl Dairy" # likely a separate thing from other categorizing
if veg:
	category = "V"
if non_dairy:
	dairy = "Non-Dairy"
if vegan: # order of these statements matters -- if vegan, is also veg, but veg + vegan != non-dairy if non-dairy has meat
	category = "V2"
if not vegan and not veg:
	category = "O" # anything with meat is Omnivorous, may also be non-dairy


#### TEST printing
print file_title
print title, ";", category, ";", dairy
print "url: <%s>" % test_recipe 

print "\nIngredients Needed:"
for i in ingredient_strs:
	print "* %s" % i 

print "\nDIRECTIONS:"
#print alldirs
for l in alldirs.split(". ")[:-1]:
	print "-> %s." % l
print "-> %s" % alldirs.split(". ")[-1] # last one won't take off "."

# save in text file
f = open(file_title, "w") # create new file (unless exists already)
# create string
recipe_str = "%s; %s; %s\nurl: <%s>\n\nIngredients Needed:\n" % (recipe_title, category, dairy, test_recipe)
for i in ingredient_strs:
	recipe_str += "\n* %s" % i
recipe_str += "\n\nDIRECTIONS:"
for l in alldirs.split(". ")[:-1]:
	recipe_str += "\n-> %s." % l
recipe_str += "\n-> %s" % alldirs.split(". ")[-1]

f.write(recipe_str)

## Create Document
