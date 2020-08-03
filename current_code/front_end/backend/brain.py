print('Brain import: importing external modules\n Importing subprocess module')
import subprocess #for executing speaking on windows (unlikely to be used again as spninx doesnt work v well on windows)
print('importing yalm module')
import yaml #for passiing profile
print('importing os module')
import os
print('importing sys module')
import sys
print('importing nltk modules')
import nltk
print('importing lexical algorithms')
import lexicalmisc
from nltk import PorterStemmer
print('importing sqlite3')
import sqlite3 as lite
print('enternal modules imported: commencing greymatter module import.')
from greymatter import general_conversations,time,weatherf,wikicode
print('grey matter successfully imported')

splittext1=[]
def wordsearch(wordlist):
    newwordlist2=search(wordlist,"key_words")
    newwordlist2=resetnonewords(newwordlist2,wordlist)
    newwordlist2=search(wordlist,"generalwords")
    idlist=[]
    for i in newwordlist2:
        if type(i) is list:
            idlist.append(i[0][0])
    return (idlist,newwordlist2)

def resetnonewords(wordlist,words):
    n=0
    for i in wordlist:
        if i==[]:
            wordlist[n]=words[n]
        n=n+1
    return(wordlist)

def search(wordlist2,table):
    t=wordlist2
    foundwords=wordlist2
    conn=lite.connect('word_funct_db.db')
    cur=conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #print(cur.fetchall())
    statement = 'SELECT * FROM '+table+' WHERE word=? LIMIT 1;'
    j=0
    for i in wordlist2:
        if(isinstance(i, basestring))==True:
            cur.execute(statement,(i,))
            x=cur.fetchall()
            if x!=[]:
                foundwords[j]=x
        j=j+1
    return(foundwords)

def tts(message):
    if(sys.platform=='linux2'):
	import linuxspeak
    print(message)
    linuxspeak.speak(message)             #function to speak output on multiple platforms
    return message
    if(sys.platform=='win32'):
        ttsengine='espeak'
        subprocess.call("espeak -s 130 -v +f2 " +message,shell=True)
        return message

def findfunction(idlist):
    count=0
    fcount=0
    for i in idlist:
        stri=str(i)
        if int(stri[-1:])==3:
            fcount=i
        count=count+1
    return fcount

def functionsearch(wordid):
    conn=lite.connect('word_funct_db.db')
    cur=conn.cursor()
    cur.execute('SELECT pointer FROM key_words WHERE wordid=?',(wordid,))
    return(cur.fetchall())

def wsetup(funct,idlist,tags):
    global splittext1
    weatherf.idlist=idlist
    weatherf.wordlist=splittext1
    weatherf.tags=tags
    output=weatherf.weatherfselect(funct,idlist)
    return output
def gsetup(fc,idlist,tags):
    general_conversations.idlist=idlist
    output=general_conversations.gselect()
    tts(output)
    return output

def tsetup(funct,idlist,tags):
    time.idlist=idlist
    output=time.tselect(funct)
    return output
def wikisetup(funct,idlist,tags):
    global splittext1
    wikicode.wordlist=splittext1
    wikicode.idlist=idlist
    output=wikicode.setup(funct)
    return output
def changesplit(value):
    global splittext1
    splittext1=value


def brain(speech_text):
    global idlist
    splittext,tags=lexicalmisc.removestopwords(speech_text)
    idlist,wordlist=wordsearch(splittext)
    fcount=findfunction(idlist)
    fc=functionsearch(fcount)
    if fc==[]:
        output=gsetup(fc,idlist,tags)
        return output
    fc=str((fc[0][0]))
    counter=0
    change=''
    ffull=fc
    for i in fc:
        try:
            j=int(i)
            if change=='':
                change=counter
        except ValueError:
                counter=counter+1
    #print(fc,change,1)
    if(change!=''):fc=fc[0:change]
    splittext,tags=lexicalmisc.removestopwords(speech_text)
    changesplit(splittext)
    output=maindict[fc](ffull,idlist,tags)
    tts(output)
    return output

maindict={
    'W':wsetup,
    'G':gsetup,
    'T':tsetup,
    'WIKI':wikisetup
}
#brain('what is the time')