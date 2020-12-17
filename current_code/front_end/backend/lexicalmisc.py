import nltk
from nltk.tag import pos_tag, map_tag
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
text='what is the weather in london'.split()
taggedtext= (nltk.pos_tag(text))
simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in taggedtext]

#print(simplifiedTags)

def removestopwords(sentence):
	stopWords = set(stopwords.words('english'))
	words = sentence.split()
	wordsFiltered = []

	for w in words:
		if w not in stopWords:
			wordsFiltered.append(w)
	tags=nltk.pos_tag(wordsFiltered)
	taglist=[]
	for i in tags:
		taglist.append(i[1])
	if wordsFiltered==[]:
		return words,taglist
	else:
		return wordsFiltered,taglist