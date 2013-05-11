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

stopwords = ["in", "on", "the", "of", "what"] # extend / grab from elsewhere??

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
for lst in [x.split() for x in ingreds_dict]:
	for w in lst:
		if w in alldirs[place:] and w not in stopwords and w[-2:] != "ed": # basically never gonna want to id a verb this way -- generalization
			print "WORD: ", w
			print " ".join(lst)
			orig_place = alldirs.find(w)
			ingred = " ".join(lst)
			alldirs = alldirs.replace(w, ingred)
			place = alldirs.find(ingred) + len(ingred) + orig_place
			# now, want to skip ahead in the search: len(" ".join(lst)) - len(w)



# for k in ingreds_dict:
# 	if k in alldirs:
# 		alldirs = alldirs.replace(k, "%s %s" % (ingreds_dict[k], k)) # works just a little for things that are exactly right





#### TESTING

print title
#print srv_num

# for k in ingreds_dict:
# 	print ingreds_dict[k], k
#print check_words
#print alldirs








