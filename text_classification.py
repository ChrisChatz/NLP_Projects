# -*- coding: utf-8 -*-

import re
import twitter
import string
from nltk.tokenize import word_tokenize

def preprocessing (tweet_list):
    
    processed_voc = []
                    
    for ID,status,cat in tweet_list:
        print ID
        print status
        
        #Convert to lower case
        status = status.lower()
          
        #Convert www.* or https?://* to URL
        status = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',status)
        
        #Convert @username to atuser
        status = re.sub('@[^\s]+','atuser',status)        
        
        #Replacing punctuation with space
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        status = regex.sub(' ', status)
        
        #Replace emails with whitespace
        status = re.sub(r'[\w\.-]+@[\w\.-]+', ' ', status)
        
        #Replace #word with word
        status = re.sub(r'#([^\s]+)', r'\1', status)
        
        #Replace digits with space
        status = ''.join(i for i in status if not i.isdigit())
        
        #Remove additional white spaces
        status = re.sub('[\s]+', ' ', status)
        
        for word in status.split(' '):
            
            #Remove consecutive characters
            word = replaceTwoOrMore(word)
                            
            #Remove stopwords
            word = removeStopwords(word)
            print word
            
            if word!='':
                
                #Write word in the file
                processed_voc.append(word)
                
    return processed_voc
        
def replaceTwoOrMore(word):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", word)

def removeStopwords(word):
    stopwords = open("eng_stop_lower.txt").read()
    unigrams = word_tokenize(stopwords[:])
    for i in unigrams:
        if word==i:
            word =''
            return word

    return word
    
#Setting up Twitter API
api = twitter.Api(
 consumer_key='...',
 consumer_secret='...',
 access_token_key='...',
 access_token_secret='...'
 )

twitterTrainFile = open("100_topics_100_tweets.sentence-three-point.subtask-A.train.gold.txt", "r")
data = twitterTrainFile.readlines()

traintweets_list = []

for line in data:
    tweet = line.split()
    try:
        status = api.GetStatus(status_id = tweet[0])
        traintweets_list.append((tweet[0], status.text, tweet[1]))
    except:
        continue
    
twitterTrainFile.close()

processed_voc = preprocessing(traintweets_list)
print processed_voc 

##print traintweets_list
#negative_tweets = []
#positive_tweets = []
#neutral_tweets = []
#
#for x,y,z in traintweets_list:
#    try:
#        if z == "negative":
#            negative_tweets.append((x, y))
#        elif z == "positive":
#            positive_tweets.append((x, y))
#        elif z ==  "neutral":
#           neutral_tweets.append((x, y))
#    except:
#        print "error"
#
#for items in positive_tweets:
#        print items
