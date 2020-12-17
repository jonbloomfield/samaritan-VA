import nltk
from nltk import word_tokenize
from nltk.stem import *

def main(sentence):
	processedinput,tags,tagpairs=preprocessing(sentence)
	grammar = "NP: {<DT>?<JJ>*<NN>}"
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(tagpairs)
	print result



def preprocessing(sentence):
	tokens=word_tokenize(sentence)
	ps= PorterStemmer()
	tokenstems=[]
	for i in tokens:
		tokenstems.append(ps.stem(i))
	tags=nltk.pos_tag(tokenstems)
	taglist=[]
	tokens=[]
	for i in tags:
		tokens.append(i[0])
		taglist.append(i[1])
	return(tokens,taglist,tags)
main('tells me the times in moscows	')
