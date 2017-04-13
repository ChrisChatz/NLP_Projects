import re
import string
from nltk.tokenize import word_tokenize
import pickle 


def preprocessing (tweet_list):
    
    processed_voc = []   
                    
    for ID,status,cat in tweet_list:
        
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
            
            if word!='':  
                #Write word in the list
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

twitterTrainFile = open("Train_tweets.obj", 'rb') 
traintweets_list = pickle.load(twitterTrainFile) 

NumberOfDocuments=0
for tweet in traintweets_list:
    NumberOfDocuments+=1

twitterTrainFile.close()

processed = preprocessing(traintweets_list)

wordfreq_processed = [processed.count(w) for w in processed]

'''replace  all  the rare words of the training subset (e.g., words that do not 
occur at least 10 times in the training subset) by a special token *rare*'''
for f in range(len(wordfreq_processed)):
   if wordfreq_processed[f]<10:
       processed[f]="*rare*"
       
#create vocabulary of unique words
vocabulary=[]
counter=0
for word in processed:
    if word not in vocabulary and word!="*rare*":
        vocabulary.append(word)

 
object_pi=vocabulary
file_pi = open('Vocabulary.obj', 'w') 
pickle.dump(object_pi, file_pi) 
file_pi.close()

print "Vocabulary is created"
