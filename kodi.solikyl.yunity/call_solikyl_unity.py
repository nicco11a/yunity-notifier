import solikyl_yunity_lib
from pprint import pprint

pickups=solikyl_yunity_lib.pickups_status()
print ("Food Pickups")
pprint (pickups)
#for row in pickups:
#	#print (row)
#	print (row['store_id'])
#	print (row['date'])
print ("post")
print ("Pickup type: %s" % pickups[0]['type'])
print ("choices")
choices=[]
choices=solikyl_yunity_lib.pickup_choices(pickups)
print (choices)
print ("1 pickup")
#pickkup=[]
pickup=solikyl_yunity_lib.get_pickup(pickups, 1)
print(pickup)
print ("end")
