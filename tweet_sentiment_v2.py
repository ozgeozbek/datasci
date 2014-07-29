import sys
import json
__author__ = "Ozge Ozbek, ozgeozbek@gmail.com"
class Twitter:
	def __init__(self,tweet_file):
		self.dictionary=[] #holds all words gathered from input tweets, will not have repetitions (total number of terms in the inout data)

		
		self.stopwords=['a', 'an', 'and', 'are', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is','its', 'it','of','on','that','the', 'to','was','were','with','will','']
		self.wordcounts={}
		#self.setcounttokensofterm()
		#self.totalwordsinvocab=len(self.dictionary)#counts all words in the twitter feed - unique words
		






def hw(sent_file, tweet_file):
	scores=loadscore(sent_file)
	tweettexts=gettweettexts(tweet_file)
	calculatesentimentalltweets(tweettexts, scores)
def gettweettexts(tweet_file):
	tweets=[]
	for line in tweet_file:#replace file with sys argv here
		try:
			tweets.append(json.loads(line))
		except:
			pass
	texts = []
	for tweet in tweets:
		if 'text' in tweet:#deleted tweets seem to have no text element, so ignore 'delete'
			toappend=tweet['text']
		elif 'delete' in tweet:
			toappend='deletedTweetWithNoText'
		texts.append(toappend)
	return texts
	#return texts
def loadscore(sent_file):
	afinnfile = sent_file
	inputscores = {} # initialize an empty dictionary
	for line in afinnfile:
  		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  		inputscores[term] = int(score)  # Convert the score to an integer.
	#print inputscores.items() # Print every (term, score) pair in the dictionary
	return inputscores

def getsentimentscore(word, scores):#call loadscore(sent_file) prior to this
	if(word in scores):
		return scores[word]
	else:
		return 0 

def calculatesentiment(tweettext, scores):
	parts = tweettext.split(' ')#split the text of a given tweet into words
	sum=0
	for i in range(0,len(parts)):#get sentiment score of each word and calculate the total sum to find one tweet's sentiment
		sum=sum+getsentimentscore(parts[i].lower(), scores)
		#print sum, ' ', parts[i].lower()
	return sum
def calculatesentimentalltweets(tweettexts,scores):
	for i in range(0,len(tweettexts)):#for each tweet in the list calculate and print total sentiment, this is the output of HW
		sentiment=calculatesentiment(tweettexts[i], scores)
		print sentiment
def lines(fp):
    print str(len(fp.readlines()))

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	hw(sent_file, tweet_file)
#    lines(sent_file)
#    lines(tweet_file)

if __name__ == '__main__':
    main()
