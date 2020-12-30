from newsapi import NewsApiClient
from pandas import json_normalize
# Init
global idlist

newsapi = NewsApiClient(api_key='68b7f3d48e2045da871e917fbb5af2f8')



def top_headlines():
   global idlist
   country="gb"
   cat="general"
   for i in idlist:
      cattest=catagorydict.get(i)
      if cattest!=None:
         cat=cattest

   top_headlines =newsapi.get_top_headlines(category=cat,
   language='en',country=country)     
   top_headlines=json_normalize(top_headlines['articles'])   
   newdf=top_headlines[["title","url"]]    
   dic=newdf.set_index('title')['url'].to_dict()
   headlinelist=list(dic.keys())
   linklist=list(dic.values())
   newslist=list()
   size=len(dic)
   count=0
   while(count<size):
      newselement=(headlinelist[count],linklist[count])
      newslist.append(newselement)
      count+=1
   output=''
   for i in newslist:
      output+=(i[0]+"\n"+i[1])
   return output


def nwsselect(fc):
   global idlist
   print( idlist[0]+idlist[1])
   output=newsdict[fc]()
   return output


newsdict={
   'N1':top_headlines
}

catagorydict={
   172:"technology",
   162:"science",
   152:"health",
   142:"general",
   132:"entertainment",
   122:"business"
}