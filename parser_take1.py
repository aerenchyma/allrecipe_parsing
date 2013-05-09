# recipe parser, Take 2

import mechanize as mech 


# Browser and setting options
br = mech.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mech._http.HTTPRefreshProcessor(), max_time=1) # can I even do this? not that important

test_recipe = "http://allrecipes.com/Recipe/Mandarin-Chicken-Pasta-Salad/"

response = br.open(test_recipe)
recpt = response.read()

