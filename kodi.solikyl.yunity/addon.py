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
	line=solikyl_yunity_lib.show_status()
	ret = xbmcgui.Dialog().contextmenu(list=line)
	if (ret < 0):
		break
	ok = xbmcgui.Dialog().yesno(title+" - Details of pickup", "Choice %d: " % (ret + 1), line[ret], "", nolabel="Cancel", yeslabel="Continue",autoclose=25000)
	if (ok == False):
		break 
