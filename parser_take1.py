# recipe parser, Take 2

# TODO: indexing by ingredients, searching for "all no milk" or w/e 
# TODO: v/v2/o
# TODO: all formatting questions (bolding ingredients in final print? TeX?)
# TODO: 

###

import lxml.html as lh
import urllib2
from bs4 import BeautifulSoup


test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"
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
alldirs = " ".join([x.string for x in directions.findAll("span", "plaincharacterwrap break")])

# #check_words = [str(x) for x in alldirs.split() if x not in stopwords]
# for word in check_words:
# 	if word in ingreds_dict: # this will not work unless they're exactly the same though
# 		# also bigrams like "sesame oil" are a problem
# 		# should direct FROM the dict -- if that string is in the alldir string
# 		alldirs.replace(word, "%s %s" % (ingreds_dict[word], word))
place = 0
# for lst in [x.split() for x in ingreds_dict]:
# 	for w in lst:
# 		if w in alldirs[place:] and w not in stopwords and w[-2:] != "ed": # basically never gonna want to id a verb this way -- generalization
# 			print "PLACE:", place
# 			print "WORD: ", w
# 			print " ".join(lst)
# 			orig_place = alldirs.find(w)
# 			ingred = " ".join(lst)
# 			alldirs = alldirs.replace(w, ingred)
# 			place += alldirs.find(ingred) + len(ingred) + orig_place - len(w)
# 			#print "PLACE: ", place
# 			# now, want to skip ahead in the search: len(" ".join(lst)) - len(w)
replaced = []
for w in [x for x in alldirs.split() if x != "" and x != " " and x not in stopwords and x[-2:] != "ed"]:
	for ig_wlst in [y.split() for y in ingreds_dict]:
		if w in ig_wlst and w not in replaced:
			place = alldirs.find(w,place) + len(" ".join(ig_wlst))# plus some amount...?? 
			alldirs = alldirs.replace(w, " ".join(ig_wlst))
			replaced += ig_wlst


# look for double words in alldirs and replace them
def word_sans_comma(w):
	return w.replace(",","")


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
#print srv_num

# for k in ingreds_dict:
# 	print ingreds_dict[k], k
#print check_words
print alldirs








