from __future__ import division
import sys
import json
from collections import defaultdict
import operator

__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
class Twitter:
	def __init__(self,tweet_file, sent_file):
		self.scores=self.loadscore(sent_file) #known words and sentiments 
		self.tweettexts=self.gettweettexts(tweet_file)	
		self.vocabulary=[] #holds all words gathered from input tweets, will not have repetitions (total number of terms in the inout data)
		self.stopwords=['a', 'an', 'and', 'are', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is','its', 'it','of','on','that','the', 'to','was','were','with','will','']
		self.wordcounts={} # it holds positive versus negative word counts
		self.unknownwords=[]
		self.classdictionary=self.calculatesentimentalltweets(self.tweettexts, self.scores)#old dict var, holds pos and neg classes
		#self.setcounttokensofterm()
		#self.totalwordsinvocab=len(self.dictionary)#counts all words in the twitter feed - unique words
		



 	def hw(self,sent_file, tweet_file):
# 		scores=loadscore(sent_file) #known words and sentiments 
# 		tweettexts=gettweettexts(tweet_file)
# 		dict=calculatesentimentalltweets(tweettexts, scores) #here we have classified all tweets into groups based on each tweets total sentiment value
# 		#completedict=createvocabulary(dict)
# 		unknownwords=findunknownwords(completedict, scores)
		self.findsentimentofunknown()
# 	#find now the probability of an unknown word having a positive sentiment given it is in a tweet with positive sentiment
	def gettweettexts(self,tweet_file):
		tweets=[]
		for line in tweet_file:#replace file with sys argv here
			try:
				tweets.append(json.loads(line))
			except:
				pass
		texts = []
		for tweet in tweets:
			if 'text' in tweet:#deleted tweets seem to have no text element, so ignore 'delete'
				texts.append(tweet['text'])
		return texts
	def loadscore(self,sent_file):
		afinnfile = sent_file
		inputscores = {} # initialize an empty dictionary
		for line in afinnfile:
			term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
			inputscores[term] = int(score)  # Convert the score to an integer.
		#print inputscores.items() # Print every (term, score) pair in the dictionary
		return inputscores

	def getsentimentscore(self,word, scores):#call loadscore(sent_file) prior to this
		if(word in scores.keys()):
			return scores[word]
		else:
			if (word not in self.unknownwords):
				self.unknownwords.append(word)
			return 0 
	def isstopword(self,term):
		stopwords=['a', 'an', 'and', 'are', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is','its', 'it','of','on','that','the', 'to','was','were','with','will','']
		isstop= term.lower() in stopwords
		return isstop
		
	def removestopwords(self,listoftokens):
		temptokenlist=[]
		for term in listoftokens:
			if(self.isstopword(term)==False):
				temptokenlist.append(term)
		return temptokenlist
	def calculatesentiment(self,tweet, scores):#calcluate sentiment for each word and add words into global vocabulary at the same time
		sum=0
		for word in tweet:#get sentiment score of each word and calculate the total sum to find one tweet's sentiment
			sum=sum+self.getsentimentscore(word, scores)
		return sum
	def createlistfromtweet(self,tweettext):
		tweetwords=tweettext.encode("utf-8").lower().split(' ')
		tweetwordsclean=self.removestopwords(tweetwords)
		tweet=[]
		for term in tweetwordsclean:
			termclean=self.cleanuppunctuations(term.lower())
			if termclean not in self.vocabulary:
				if termclean is not None:
					self.vocabulary.append(termclean)
					tweet.append(termclean)
		return tweet
	def calculatesentimentalltweets(self,tweettexts,scores):#this creates 3 sentiment classes for input tweets
		classification=defaultdict(list)
		for i in range(0, len(tweettexts)):#for each tweet in the list calculate and print total sentiment, this is the output of HW
			tweet=self.createlistfromtweet(tweettexts[i])
			sentiment=self.calculatesentiment(tweet, scores)
			value=(tweet, sentiment)
			if sentiment>0:
				key='positive'
				classification[key].append(value)
			elif sentiment<0:
				key='negative'
				classification[key].append(value)
			elif sentiment==0:
				key='neutral'
				classification[key].append(value)
		#print sentiment
		return classification
	# def createvocabulary(d):
	# 	worddictionary=[]
	# 	for k,kvals in d.iteritems():# d is a defaultdict with class, tweettext and sentiment score
	# 		for vals in kvals:
	# 			tweetwords=operator.itemgetter(0)(vals).encode("utf-8").lower().split(' ')
	# 			tweetwordsclean=removestopwords(tweetwords)
	# 			for term in tweetwordsclean:
	# 				if term.lower() not in worddictionary:
	# 					termclean=cleanuppunctuations(term.lower())
	# 					if termclean is not None:
	# 						worddictionary.append(termclean)
	# 	return worddictionary
		
	#def cleanuppunctuations(word):
	#	punctuations = '''!()-[]{};:'"\/,<>./?@#$%^&*_~'''
	#	cleaned_up = ""
	#	for char in word:
	#		if char not in punctuations:
	#			cleaned_up = cleaned_up + char
	#	return cleaned_up
	def cleanuppunctuations(self,word):
		if all(ord(c)> 65 and ord(c) <= 122 for c in word)==True:
			return word

	def calcoccurances(self,wordlist):
		return len(wordlist)
	def isunknown(self,word,scores):
		if(word in scores):
			return False
		else:
			return True
	def findunknownwords(self,worddict, scores):
		unknown=[]
		for word in worddict:
			if(isunknown(word,scores)==True):
				unknown.append(word)
		return unknown
	def createdictfromtweets(self, classname):
		worddictionary=[]
		for vals in self.classdictionary[classname]:
			worddictionary.append(operator.itemgetter(0)(vals))
		return worddictionary
	def findtotalsentimentscore(self,word,dict):
		sumscores=0
		for k,kvals in dict.iteritems():# d is a defaultdict with class, tweettext and sentiment score
			for vals in kvals:
				tweetwords=operator.itemgetter(0)(vals)
				for term in tweetwords:
					if term is not None:
						if term==word:
							sumscores+=operator.itemgetter(1)(vals)
		return sumscores
	def countunknowninclass(self,word, sentimentclass):
		count=0
		for i in sentimentclass:
			if (word==i):
				count+=1
		return count
	def findsentimentofunknown(self):
		vocabularylen=len(self.vocabulary)
		dict_pos=self.createdictfromtweets('positive')
		dict_neg=self.createdictfromtweets('negative')
		numberofwordsinpositive=self.calcoccurances(dict_pos)
		numberofwordsinnegative=self.calcoccurances(dict_neg)
		for word in self.unknownwords:
			positive=self.countunknowninclass(word, dict_pos)
			negative=self.countunknowninclass(word, dict_neg)
			sentiment_pos=(positive+1)/(numberofwordsinpositive+vocabularylen)
			sentiment_neg=(negative+1)/(numberofwordsinnegative+vocabularylen)
			score=self.findtotalsentimentscore(word,self.classdictionary)
			finalscore=score*(sentiment_pos/sentiment_neg)
			print word, finalscore
	def lines(fp):
		print str(len(fp.readlines()))

	def main():
		sent_file = open(sys.argv[1])
		tweet_file = open(sys.argv[2])
		#hw(sent_file, tweet_file)
	#    lines(sent_file)
	#    lines(tweet_file)

	if __name__ == '__main__':
		main()
tweet_file = open(sys.argv[2])
sent_file = open(sys.argv[1])
m=Twitter(tweet_file, sent_file)
m.hw(sent_file, tweet_file)
