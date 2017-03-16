import xbmcaddon
import xbmcgui
import solikyl_yunity_lib

import warnings
warnings.filterwarnings("ignore")
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonversion	    = addon.getAddonInfo('version')

title = addonname + " (%s) " % addonversion
 
#line1 = "Solikyl - Unity!"
#line2 = "We can write anything we want here"
#line3 = "Using Python"

while (True):
	#Show the pickups in a list, you can choose one for more detials and then you can stop or continue, after 25 seconds it will cancel
	pickups=solikyl_yunity_lib.pickups_status()
	choices=[]
	choices=solikyl_yunity_lib.pickup_choices(pickups)
	#pprint (choices)
	ret = xbmcgui.Dialog().contextmenu(list=choices)
	if (ret < 0):
		break
	pickup=solikyl_yunity_lib.get_pickup(pickups, ret)
	#pprint(pickup)
	#ok = xbmcgui.Dialog().yesno(title+" - Details of pickup", "Choice %d: " % (ret + 1), choices[ret], "", nolabel="Cancel", yeslabel="Continue",autoclose=25000)
	ok = xbmcgui.Dialog().yesno(title+" - Details of pickup", "Choice %d: " % (ret + 1), pickup[0], pickup[1], nolabel="Cancel", yeslabel="Continue",autoclose=25000)
	if (ok == False):
		break 
