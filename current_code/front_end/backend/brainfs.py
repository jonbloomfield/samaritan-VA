print('Brain import: importing external modules\n Importing subprocess module')
import subprocess #for executing speaking on windows (unlikely to be used again as spninx doesnt work v well on windows)
print('importing yalm module')
#import yaml #for passiing profile
print('importing os module')
import os
print('importing sys module')
import sys
print('importing nltk modules')
import nltk
print('importing lexical algorithms')
from . import lexicalmisc
from nltk import PorterStemmer
print('importing sqlite3')
import sqlite3 as lite
print('enternal modules imported: commencing greymatter module import.')
from . greymatter import general_conversations,timef,weatherf,wikicode,newsfs,calendarcode
print('grey matter successfully imported')

import os.path
splitwordlist=[]

def wordsearch(wordlist):
    newwordlist2=search(wordlist,"key_words")
    newwordlist2=resetnonewords(newwordlist2,wordlist) #searches for words
    newwordlist2=search(wordlist,"generalwords")
    idlist=[]
    for i in newwordlist2:
        if type(i) is list:
            idlist.append(i[0][0])
    return (idlist,newwordlist2)

def resetnonewords(wordlist,words): #got none with split, this removes none vals from lists
    n=0
    for i in wordlist:
        if i==[]:
            wordlist[n]=words[n]
        n=n+1
    return(wordlist)

def search(wordlist2,table):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # get absolute path for so no path issues
    db_path = os.path.join(BASE_DIR, "word_funct_db.db")
    t=wordlist2
    foundwords=wordlist2
    conn=lite.connect(db_path)
    cur=conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")   #accesses db
    statement = 'SELECT * FROM '+table+' WHERE word=? LIMIT 1;'
    j=0
    for i in wordlist2:
        if(isinstance(i, str))==True:
            cur.execute(statement,(i,))
            x=cur.fetchall()
            if x!=[]:
                foundwords[j]=x
        j=j+1
    return(foundwords)

def tts(message):
    if(sys.platform=='linux'):
        from . import linuxspeak
        #print(message)
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
        if int(stri[-1:])==3: # if last char==3, word is key word
            fcount=i
        count=count+1
    return fcount

def functionsearch(wordid):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "word_funct_db.db")
    conn=lite.connect(db_path)
    cur=conn.cursor()
    cur.execute('SELECT pointer FROM key_words WHERE wordid=?',(wordid,))   #find if key word has funct accociated
    return(cur.fetchall())

def wsetup(funct,idlist,tags):  #weather setup
    global splitwordlist
    print(splitwordlist)
    weatherf.idlist=idlist      #set weather file vars to brain vars
    weatherf.wordlist=splitwordlist
    weatherf.tags=tags
    output=weatherf.weatherfselect(funct,idlist)    #get output
    return output

def gsetup(fc,idlist,tags):
    general_conversations.idlist=idlist #geenral setup, set general file vars to brain ones
    output=general_conversations.gselect()
    return output

def tsetup(funct,idlist,tags):
    timef.idlist=idlist      #time setup
    output=timef.tselect(funct)
    return output
def wikisetup(funct,idlist,tags):
    global splitwordlist
    wikicode.wordlist=splitwordlist    #wiki setup
    wikicode.idlist=idlist
    output=wikicode.setup(funct)
    return output
def newssetup(funct,idlist,tags):
    #print("testcompelre")
    newsfs.idlist=idlist
    output=newsfs.nwsselect(funct)
    return output
def calandersetup(funct,idlist,tags):
    global splitwordlist
    print(idlist,splitwordlist)
    calendarcode.idlist=idlist
    calendarcode.wordlist=splitwordlist
    output=calendarcode.cselect()
    return output

def brain(speech_text):
    global idlist
    global splitwordlist
    splittext,tags=lexicalmisc.removestopwords(speech_text)
    splitwordlist,tags=lexicalmisc.removestopwords(speech_text)
     #remove stop words, splits
    idlist,wordlist=wordsearch(splittext)
    print(idlist,wordlist)   #send split text, get id + key words
    fcount=findfunction(idlist)
    print(fcount) #search for key word functs
    fc=functionsearch(fcount)   #go to funct via funct id
    if fc==[]:
        print(0)
        output=gsetup(fc,idlist,tags)   #if no id recognised, go to general convos (dont understand etc)
        return output
    fc=str((fc[0][0])) # formatting
    counter=0
    change=''
    ffull=fc
    for i in fc:    #formatting func string, certain characters=split
        try:
            j=int(i)
            if change=='':
                change=counter
        except ValueError:
                counter=counter+1
    if(change!=''):fc=fc[0:change]
    output=maindict[fc](ffull,idlist,tags)  #use maindict to go to corrent pelim funct
    return output

maindict={
    'W':wsetup, #funct dict
    'G':gsetup,
    'T':tsetup,
    'WIKI':wikisetup,
    'N':newssetup,
    'C':calandersetup
}

brain("set alarm for 11:00")