from __future__ import division
import math
import operator
import sys
import json
from collections import Counter
from collections import defaultdict

class Twitter:
	def __init__(self,tweet_file):
		self.dictionary=[] #holds all words gathered from input tweets, will not have repetitions (total number of terms in the inout data)
		self.states = {
        'Alaska':'AK',
        'Alabama':'AL',
        'Arkansas':'AR',
        'American Samoa':'AS',
        'Arizona':'AZ',
        'California':'CA',
        'Colorado':'CO',
        'Connecticut':'CT',
        'District of Columbia':'DC',
        'Delaware':'DE',
        'Florida':'FL',
        'Georgia':'GA',
        'Guam':'GU',
        'Hawaii':'HI',
        'Iowa':'IA',
        'Idaho':'ID',
        'Illinois':'IL',
        'Indiana':'IN',
        'Kansas':'KS',
        'Kentucky':'KY',
        'Louisiana':'LA',
        'Massachusetts':'MA',
        'Maryland':'MD',
        'Maine':'ME',
        'Michigan':'MI',
        'Minnesota':'MN',
        'Missouri':'MO',
        'Northern Mariana Islands':'MP',
        'Mississippi':'MS',
        'Montana':'MT',
        'National':'NA',
        'North Carolina':'NC',
        'North Dakota':'ND',
        'Nebraska':'NE',
        'New Hampshire':'NH',
        'New Jersey':'NJ',
        'New Mexico':'NM',
        'Nevada':'NV',
        'New York':'NY',
        'Ohio':'OH',
        'Oklahoma':'OK',
        'Oregon':'OR',
        'Pennsylvania':'PA',
        'Puerto Rico':'PR',
        'Rhode Island':'RI',
        'South Carolina':'SC',
        'South Dakota':'SD',
        'Tennessee':'TN',
        'Texas':'TX',
        'Utah':'UT',
        'Virginia':'VA',
        'Virgin Islands':'VI',
        'Vermont':'VT',
        'Washington':'WA',
        'Wisconsin':'WI',
        'West Virginia':'WV',
        'Wyoming':'WY'
}
		
		self.stopwords=['a', 'an', 'and', 'are', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is','its', 'it','of','on','that','the', 'to','was','were','with','will','']
		self.wordcounts={}
		#self.setcounttokensofterm()
		#self.totalwordsinvocab=len(self.dictionary)#counts all words in the twitter feed - unique words
		

# Load data
	def gettweettextslocations(self, tweet_file):
		tweets=[]
		for line in tweet_file:
			try:
				tweets.append(json.loads(line))
			except:
				pass
		locationtext = {}
		for tweet in tweets:
			if 'place' in tweet:
				if tweet['place'] is not None:#place should not be null
					if tweet['place']['country_code']=='US':
						key=tweet['id_str']
						state=self.getstate(tweet['place']['full_name'])
						locationtext[key]=(state,tweet['text'])
						#for loc in location:
							#if len(loc)!=0:
							#texts.append(location['text'].encode("utf-8") )
		return locationtext
	def getstate(self, location): 
		parts = location.split(', ')
		if parts[1]=='USA':
			if parts[0] in self.states:
				return self.states[parts[0]]
			else:
				return 'N/'
		else: 
			return parts[1]
	def loadscore(self,sent_file):
		afinnfile = sent_file
		inputscores = {} # initialize an empty dictionary
		for line in afinnfile:
			term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
			inputscores[term] = int(score)  # Convert the score to an integer.
		#print inputscores.items() # Print every (term, score) pair in the dictionary
		return inputscores

	def getsentimentscore(self,word, scores):#call loadscore(sent_file) prior to this. Returns the sentiment of a word.
		if(word in scores):
			return scores[word]
		else:
			return 0 

	def calculatesentiment(self,tweettext, scores):
		parts = tweettext.split(' ')#split the text of a given tweet into words
		sum=0
		for i in range(0,len(parts)):#get sentiment score of each word and calculate the total sum to find one tweet's sentiment
			sum=sum+self.getsentimentscore(parts[i].lower(), scores)
			#print sum, ' ', parts[i].lower()
		return sum
	def calculatesentimentalltweets(self,tweetdict,scores):
		statesentiment=defaultdict(list) #to hold the sentiment values per state
		for key in tweetdict:#for each tweet in the list calculate total sentiment
			sentiment=self.calculatesentiment(tweetdict[key][1], scores)
			statesentiment[tweetdict[key][0]].append(sentiment)
		return statesentiment
	def lines(self,fp):
		print str(len(fp.readlines()))
	def findhappiest(self, statesentimentdict):
		avgsentdict={k: sum(vals) / len(vals) for k, vals in statesentimentdict.viewitems()}
		return max(avgsentdict, key=avgsentdict.get)
	def hw(self,sent_file, tweet_file):
		scores=self.loadscore(sent_file)
		tweettextslocations=self.gettweettextslocations(tweet_file)
		#print tweettextslocations
		defdict=self.calculatesentimentalltweets(tweettextslocations, scores)
		print self.findhappiest(defdict)
tweet_file = open(sys.argv[2])
sent_file = open(sys.argv[1])
m=Twitter(tweet_file)
m.hw(sent_file, tweet_file)

