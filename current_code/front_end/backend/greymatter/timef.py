print('importing time module')
from datetime import datetime
import time
global idlist

def tell_time(name):
	datestring=datetime.strftime(datetime.now(),'%H:%M')
	return("The time is " + datestring.replace(':',' ')) #pretty obvious

def tell_date(name):
	datestring=datetime.strftime(datetime.now(), '%A:%d:%B:%Y')
	datestring=datestring.replace(':',' ')
	return ("The date is " + datestring) #pretty obvious
print('imported time time module')

def tselect(fc):
	global idlist
	output=tdict[fc](0)
	return output
tdict={
	'T1':tell_time,
	'T2':tell_date

}