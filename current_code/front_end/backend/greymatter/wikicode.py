import wikipedia

wordlist=[]
idlist=[]

def summary(word,flag):
	try:
		definitionfull=wikipedia.summary(word)
	except:
		return("unable to connect to wikipedia.  I suggest opening a book.")
	if flag==0:
		defsplit=definitionfull.split('. ')
		newdef=defsplit[0:1]
		enddef=''
		for i in newdef:
			enddef=enddef+i+'. '
		return(enddef)
	else: return definitionfull


def wiklex():
	global wordlist
	global idlist
	DorSflag=None
	dcount=0
	count=0
	for i in wordlist:
		if i=='define':
			dcount=count
			DorSflag=0
		elif i=='summary':
			dcount=count
			DorSflag=1
		count=count+1
	return dcount,DorSflag


def setup(funct):
	dcount,DorSflag=wiklex()
	output=summary(wordlist[dcount:],DorSflag)


	return output

#summary('star')