print('importing weather module')
import pyowm
import time
import datetime
owm = pyowm.OWM("b8650f4b75d74e34750b328562caf547")  # API key for open weather api
mgr = owm.weather_manager()
cacheweather=''

idlist=[]
wordlist=[]
tags=[]
loc='london'
tomorrow=False


def checkcache():
	return True
	if(cacheweather==''): 
		return True
	timenow=time.time()
	cachetime=cacheweather.get_reference_time()		#samaritan keeps a recent weather cache to save on html request numbers and speed
	diff=timenow-cachetime
	if(diff>7200):return True 	#if defference is more than 3 hrs (when the free weather api service updates)
	else: return False

def currentweather(): #function for current weather
	global cacheweather
	global loc
	if checkcache()==True:					#if new cache needed
		obs = mgr.weather_at_place(str(loc)+", UK")                    
		w = obs.weather
		cacheweather=w
		return ('today, there will be '+w.detailed_status)
	elif checkcache()==False:
		return ('today, there will be '+cacheweather.detailed_status)	#if cache recent, pull from cache

def getemperature():
	global loc
	global cacheweather
	if checkcache()==True:
		obs = mgr.weather_at_place(str(loc)+',uk')                   # if new cache needed
		w = obs.get_weather()
		cacheweather=w
		temp=w.get_temperature(unit='celsius')
		tempmin=str(format(temp['temp_min']))		#pull temperature figures from raw data
		tempmin=tempmin[0:-2]
		tempmax=str(format(temp['temp_max']))
		tempmax=tempmax[0:-2]
		return ('today in '+loc+', the temperature will be between '+tempmin+' degrees and '+tempmax+' degrees')
	elif checkcache()==False:
		temp=cacheweather.get_temperature(unit='celsius')
		tempmin=str(format(temp['temp_min']))
		tempmin=tempmin[0:-2]								#pull temperature figures from raw data
		tempmax=str(format(temp['temp_max']))
		tempmax=tempmax[0:-2]
		print('cahce')
		return ('today, the temperature will be between '+tempmin+' degrees and '+tempmax+' degrees')

def feature_today(): #function to tell if particular weather feature will be present in the next 24 hrs
	global idlist
	global loc
	global tomorrow
	global tags
	feature=''
	for i in idlist:
		if i in featuredict.keys():
			feature=i
	feature=featuredict[feature]
	try:
		fc = mgr.three_hours_forecast(str(loc)+',uk')
	except:
		return("error connecting to weather network. I suggest you look outside")
	f = fc.get_forecast()
	lst = f.get_weathers()
	lst=lst[0:4] 	#*NOTE : update list for tomorrow, currently only getting 1st 24 hrs
	now=datetime.datetime.now()
	neededdate=now.strftime("%Y-%m-%d") 
	datestring=' today'
	if(tomorrow==True):	
		neededdate=datetime.date.today() + datetime.timedelta(days=1)	#can do ask for tomorrow or today. 
		datestring=' tomorrow'
	for i in lst:
		date=i.get_reference_time(timeformat='date')
		if(date.date()==neededdate):
			status=i.get_detailed_status()
			if set(feature).issubset(set(status)):
				return ('Yes, there will be '+feature+datestring)
		return ('No, there will not be '+feature+datestring)
print('weather module imported')

def exists(wordid):
	global idlist
	for i in idlist:
		if i == wordid:
			return True
	return False

def weatherfselect(funct,idlist):
	global wordlist
	global lastidlist
	global tomorrow
	global loc
	global tags
	lastidlist=idlist
	if exists(102):
		tomorrow=True
	if exists(92):
		tomorrow=False
		print("here")

	locpointer=''					#find location via speech format and change loc to current location
	count=len(tags)-1
	print(tags)
	print(count)
	print(wordlist)
	print(funct)
	print(idlist)
	while(count>=0):
		if tags[count]=='NN' and locpointer=='' and (wordlist[count]!='today'):
			locpointer=count
		count=count-1
	#print(wordlist)
	loc=wordlist[locpointer]
	print(loc)

	output=weatherdict[funct]()
	return output


weatherdict={
'W1':currentweather,
'W2':getemperature,
'W3':feature_today
}

featuredict={
	73:'snow',
	93:'rain',
	103:'fog',
	113:'cloud',
	123:'sun'

}
