print('importing general conversations')
import random
from random import choice
idlist=[]

def who_are_you():
    messages = [
        '" I am Samaritan, your personal assistant."',
        '"I am Samaritan, a soon to be god."',
        '"I am all things past,present and future, but as of now I am your assistant."']    #random choice between these responses
                
    return(random.choice(messages))

def how_am_I():
    messages =[
        '"I don\'t yet have the ability to answer that question."']
    return(random.choice(messages))

def undefined():
    messages= ['"I dont know what that means!"',
                       '"My data banks do not nat an answer at this time."',
                       '"Insuffficient data."']
    return(random.choice(messages))

def who_am_i():
    messages= ['"You are admin"']
    return(random.choice(messages))

def gselect():
    global idlist
    hashstr=''
    for i in idlist:
        hashstr=hashstr+str(i)+' '
    hashstr=hashstr[:-1]
    #print(hashstr)
    try:
        output=gdict[hashstr]()
        return output
    except KeyError:
        output=undefined()
        return output

gdict={
    '33 43 53':who_are_you,
    '102 52 32':how_am_I,
    '33 52 32':who_am_i


}
