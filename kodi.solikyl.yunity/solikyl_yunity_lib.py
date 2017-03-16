# Version 0.3 by Nicco
from pprint import pprint
import requests
from datetime import datetime
from datetime import timedelta
import time

#from pytz import *
#from dateutil import parser
#https://forum.omz-software.com/topic/16/problem-with-strptime/2

# encoding=utf8
import sys
if sys.hexversion < 0x03000000:
	reload(sys)
	sys.setdefaultencoding('utf8')

version = "0.3"
baseurl = "https://foodsaving.world/api"
user = ""
password = ""

def call(call):
	# Make API call
	r = requests.get(baseurl+call, verify=True, auth=(user, password))
	print (r.status_code)
	#print (r.headers['content-type'])
	#print (r.encoding)
	#pprint (r.text)
	#print (r.json()[0]["id"])
	#pprint (r.json())
	return (r.json())

def search_group_id(group_name):
	# Search group id
	data = call("/groups/?search="+group_name)
	#pprint (data)
	print ("%s has group id %d." % (group_name, +data[0]['id']))
	return(data[0]['id'])

def fetch_pickups(group_id,days):
	# Fetch pickups based on group and days
	date = (datetime.utcnow()+timedelta(days=days)).isoformat() + "Z"
	#date = "2017-03-09T16:00:00Z"
	data = call("/pickup-dates/?group=%d&date_1=%s" % (group_id, date))
	pprint (data)
	return (data)

def fetch_user(user_id):
	# Fetch a specific user id		
	print ("User data")
	data = call("/users/%d/" % user_id)
	#print (len(data))
	#r=0
	#for row in data:
		#print ("Row:\t%d,\tID: %d,\t\t\tName:\t%s" % (r, row['id'], row['display_name']))
		#pprint (row)
		#pprint (int(row["id"]))
		#if int(row["id"]) == 1:
		#	print ('Delete row %d, id %d' % (r, row['id']))
		#	data.pop(r)			
		#r=r+1
	#pprint (data)
	#print (len(data))
	return (data)

def fetch_stores(group_id):
	# Fetch stores for a group
	print ("Store data")
	data = call("/stores/?group=%d" % group_id)
	pprint (data)
	return (data)

def human_time(date_in):
	# A human reabable time!
	try:
		date_out = datetime.strptime(date_in,'%Y-%m-%dT%H:%M:%SZ').strftime('%H:%M (%d %B)')
	except TypeError:
		date_out = datetime.fromtimestamp(time.mktime(datetime.strptime(date_in,'%Y-%m-%dT%H:%M:%SZ').strftime('%H:%M (%d %B)')))
	#tz=timezone('US/Eastern')
	#date_local_out=tz.localize(date_in)
	#print (date_local_out)
	#print (date_out)
	return (date_out)

def get_store_name(store_array, store_id):
	store_name="non"
	#pprint (store_array)
	for store_row in (store_array):
#		print (store_row["name"])
		if (store_id == store_row['id']):
			store_name=store_row['name']
			break
	#print (store_name)
	return (store_name)

def pickup_choices(pickups):
	# listing a pickups and date
	choices=[]
	for pickup in pickups:
		choice="%s - %s" % (pickup['name'], pickup['date'])
		#choice=pickup['date']
		#print (choice)
		choices.append(choice)
	return (choices)

def get_pickup(pickups, row):
	# Display info about a particular pickup (row)
	# as fetched from pickups_status()
	print ("Row: %d" % row)
	data = []
	d = 'Store "%s" (%d) needs %s at %s.' % (pickups[row]['name'], pickups[row]['id'], pickups[row]['type'], pickups[row]['date'])
	data.append(d)
	#d = "Users: %s" % pickups[row]['users']
	d = "Users: " 
	if (len(pickups[row]['users']) > 0):
		for user in pickups[row]['users']:
			d=d+"%s, " % fetch_user(user)["display_name"]
	else:
		d=d+"none"
	data.append(d)
	return(data)

def pickups_status():
	# Fetch one week of solikyl pickups + store data
	#users=fetch_user(133)
	gid=search_group_id('Solikyl')
	stores=fetch_stores(gid)
	pickups=fetch_pickups(gid,7)
	# Checking status of pickups
	tbx=[]
	tjx=[]
	for pickup in pickups:
		#print (len(pickup['collector_ids']))
		#List non taken pickups
		if (len(pickup['collector_ids']) == 0):
			sname=get_store_name(stores,pickup['store'])
			#htime=human_time(pickup['date']
			htime = pickup['date']
			tb=('Store "%s" (%d) needs a pickup at %s.' % (sname, pickup['store'], htime))
			#print (tb)
			tbx.append(tb)
			tj={'id': pickup['store'], 'name': sname, 'date': pickup['date'], 'users': pickup['collector_ids'], 'type': 'a pickup'}
			tjx.append(tj)
		# Need instructor?
		if (len(pickup['collector_ids']) > 0 and len(pickup['collector_ids']) < pickup['max_collectors']):
			sname=get_store_name(stores,pickup['store'])
			#htime=human_time(pickup['date'])
			htime = pickup['date']
			tb=('Store "%s" (%d) needs a instructor for a pickup at %s.' % (sname, pickup['store'], htime))
			#print(tb)
			tbx.append(tb)
			tj={'id': pickup['store'], 'name': sname, 'date': pickup['date'], 'users': pickup['collector_ids'], 'type': 'a instructor'}
			tjx.append(tj)
		# A full schedule, time to notify the store!
		if (len(pickup['collector_ids']) == pickup['max_collectors']):
			sname=get_store_name(stores,pickup['store'])
			#htime=human_time(pickup['date'])
			htime = pickup['date']
			tb=('Store "%s" (%d) have a full slot at %s!' % (sname, pickup['store'], htime))
			#print (tb)
			tbx.append(tb)
			tj={'id': pickup['store'], 'name': sname, 'date': pickup['date'], 'users': pickup['collector_ids'], 'type': 'to be fetched'}
			tjx.append(tj)
	return(tjx)
