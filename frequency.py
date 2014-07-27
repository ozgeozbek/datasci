from __future__ import division
import math
import operator
import sys
import json
from collections import defaultdict
from collections import Counter
class Twitter:
	def __init__(self,tweet_file):
		self.dictionary=[] #holds all words gathered from input tweets, will not have repetitions (total number of terms in the inout data)
		self.classvocabulary=Counter() #holds all words in the tweet file, would have reps
		self.stopwords=['a', 'an', 'and', 'are', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is','its', 'it','of','on','that','the', 'to','was','were','with','will','']
		self.settweetvocabulary(self.gettweettexts(tweet_file)) # initializes all above structures related to training set
		self.wordcounts={}
		self.setcounttokensofterm()
		self.totalwordsinvocab=len(self.dictionary)#counts all words in the twitter feed - unique words
# Load data
	def gettweettexts(self, tweet_file):
		tweets=[]
		for line in tweet_file:
			try:
				tweets.append(json.loads(line))
			except:
				pass
		texts = []
		for tweet in tweets:
			if 'text' in tweet:#deleted tweets seem to have no text element, so ignore 'delete'
				texts.append(tweet['text'])
		#	elif 'delete' in tweet:
		#		toappend=''
		return texts
	def settweetvocabulary(self, tweetlist): 
	#this function loads the clean final as a dictionary
		counter=0
		#with open(tweetfile) as f:
		for tweet in tweetlist:
			parts = tweet.split(' ')
			for term in parts:
				#key= parts[0]
				#classification= parts[1]
				#doctemp = parts[2]
				#doc=doctemp[:-1]
				#doc= doc.split(' ')
				#dict[key]=(classification,doc)
				#self.concatenatetextofalldocsinclass(doc, classification)
				self.classvocabulary[term.lower()]+=1
				if term.lower() not in self.dictionary:
					self.dictionary.append(term.lower()) #this holds all the words in the dictionary - no repetitions	
	def isstopword(self, term):
		isstop= term.lower() in self.stopwords
		return isstop		
	def removestopwords(self, listoftokens):
		temptokenlist=[]
		for term in listoftokens:
			if(self.isstopword(term)==False):
				temptokenlist.append(term)
		return temptokenlist		
	def setcounttokensofterm(self):
		#for cls in self.classvocabulary:
		counts=Counter(self.classvocabulary)
		self.wordcounts=counts
		return counts
	def calcfreq(self, term):
			return self.wordcounts[term]/self.totalwordsinvocab
	def printtermfreq(self):
		for term in self.wordcounts:
			if term.isalpha():
				print  term, ' ' , '%.4f'%self.calcfreq(term)

#tweet_file = open("output_ozge.txt")
tweet_file = open(sys.argv[1])
m=Twitter(tweet_file)
m.printtermfreq()
