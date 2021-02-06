import calendar
# Create a plain text calendar
c = calendar.TextCalendar(calendar.MONDAY)
from datetime import *
from . .threadqueues import windowqueue,outputqueue
idlist=[]
wordlist=[]
from . .security.secfs import profiledata
def setalarm():
	global wordlist
	alarmtime=""
	for i in wordlist:
		if ":" in i:
			alarmtime=i
	alarmid=1
	for i in profiledata[3]:
		if(alarmid<=i[1]):
			alarmid=i[1]+1

	profiledata[3].append([i,alarmid])
	return "alarm set for "+i
	

	


def cselect():
	global idlist
	global wordlist
	idstring=""
	for i in idlist:
		idstring+=str(i)+" "
	functkey=calendarworddict[idstring]
	output=calendarfunctdict[functkey]()
	return output	

def current_month():
	str = c.formatmonth(2019, 9, 0, 0)
	print(str)

def calendarcheck():
	timestring=datetime.strftime(datetime.now(),'%H:%M')
	for i in profiledata[3]:
		if(i[0])==timestring:
			windowqueue.put(["A",i])
			i[0]=datetime.strftime("%H:%M", datetime.localtime(time()+60))
			outputqueue.put(["ALARM FOR "+timestring+"!! INPUT DISMISS OR SNOOZE"])
	return



calendarworddict={
"182 163 ":"C2",
"192 163 ":"C2"

}

calendarfunctdict={
	"C1":current_month,
	"C2":setalarm
}

