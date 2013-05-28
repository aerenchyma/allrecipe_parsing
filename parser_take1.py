# recipe parser, Take 2

# TODO: indexing by ingredients, searching for "all no milk" or w/e 
# TODO: v/v2/o
# TODO: all formatting questions (bolding ingredients in final print? TeX?)
# TODO: 

###

import urllib2
from bs4 import BeautifulSoup
import re
import sys


def word_sans_comma(w):
	if w[-1] =="," or w[-1] == ".":
		w = w.replace(",","") # because replacing is destructive and need non-destructive fxn
		w = w.replace(".","")
	return w

# def check_repl(match_str, w):
# 	check = match_str.group(0).replace(w, "")
# 	if check != "":
# 		return 

## recipe url entering options 
#test_recipe = sys.argv[1]
#test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
test_recipe = "http://allrecipes.com/recipe/best-chocolate-chip-cookies/"

rec_doc = BeautifulSoup(urllib2.urlopen(test_recipe))
ingreds_dict = {}

stopwords = ["in", "on", "the", "of", "what", "and", "&", "are", "you", "a", "an", "or", "why"] # extend / grab from elsewhere later TODO

title = rec_doc.title.string.strip().replace(" - Allrecipes.com","")
srv_num = rec_doc.find(id="lblYield").string
test_ingr = rec_doc.findAll("p", {"class" : "fl-ing"}) 

for grp in test_ingr:
	if grp.find(id="lblIngAmount") is not None and grp.find(id="lblIngName") is not None:
		amt, nm = (grp.find(id="lblIngAmount").string, grp.find(id="lblIngName").string)
		amount_ingredient = "%s %s" % (amt, nm)
		ingreds_dict[nm.encode('utf-8')] = amt.encode('utf-8') # need to keep track of ingredient names for instrs
		# hash -> mongodb?? for indexing? a thought

directions = rec_doc.find("div", "directions")
alldirs = " ".join([x.string for x in directions.findAll("span", "plaincharacterwrap break")])

place = 0

## TODO: if you've replaced WITH the same word twice, stop replacing it -- it's silly
## are there indicators besides "the" (which doesn't work b/c recipe is already context)? unlikely.

# also, still missing things as of night 2013/05/21

# keep track of words that have been replaced to avoid unfortunate doubling
replaced = []
new_dirs_lines = []
punct_add = " "
for w in [x.encode('utf-8') for x in alldirs.split() if x != "" and x != " " and "ed" not in x[-3:] and x not in stopwords]:
	print "w is:", w
	for ig_wlst in [y.split() for y in ingreds_dict]:
		ig_wlst = [x.encode('utf-8') for x in ig_wlst]
		if (word_sans_comma(w) in ig_wlst or w in ig_wlst) and word_sans_comma(w.encode('utf-8')) not in [x.encode('utf-8') for x in replaced] and w.encode('utf-8') not in [x.encode('utf-8') for x in replaced]: #and w.encode('utf-8') not in " ".join(ig_wlst): # TODO improve consistency of encoding
			subst_str = ingreds_dict[" ".join(ig_wlst)] + " " + " ".join(ig_wlst) + " " # note spacing changes -- TODO make neater/clearer what's going on
			if w[-1] == ".":
				punct_add = ". "
			elif w[-1] == ",":
				punct_add = ", "
			alldirs = re.sub(re.escape(w) + r"[^a-zA-Z]", " " + " " + subst_str + " " if w[-1].isalnum() and punct_add != "" else subst_str.rstrip() + punct_add, alldirs) # assume if isalnum, no punct_add -- safe?
			place = alldirs.find(w,place) + len(" ".join(ig_wlst)) # correct amt

			replaced += [x.encode('utf-8') for x in ig_wlst] # working now

#print replaced

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
print replaced







