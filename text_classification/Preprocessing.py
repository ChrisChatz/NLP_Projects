import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

def preprocessing (status):
    
    #Load Stemmer
    stemmer = SnowballStemmer("english")
        
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
    
    unigrams = word_tokenize(status)
    
    #Remove consecutive characters
    unigrams = [replaceTwoOrMore(t) for t in unigrams]
    
    #Remove stopwords
    unigrams = [removeStopwords(t) for t in unigrams]
    
    #Stemming
    unigrams = [stemmer.stem(t) for t in unigrams]
    
    status = ' '.join(unigrams)
    
    #Remove additional white spaces
    status = re.sub('[\s]+', ' ', status)
    
    return status

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