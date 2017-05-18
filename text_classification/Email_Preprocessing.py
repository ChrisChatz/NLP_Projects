import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

def preprocessing (email):
    
    #Load Stemmer
    stemmer = SnowballStemmer("english")
    
    #Convert www.* or https?://* or http?://* in lower or upper case to "url"
    email = re.sub('(((?i)(www\.[^\s]+)|(?i)(https?://[^\s]+))|(?i)(http?://[^\s]+))','url', email)
    
    #Remove emails
    email = re.sub(r'[\w\.-]+@[\w\.-]+', '', email)     
    
    #Remove the word "Subject" only from the beginning of the emails
    email = re.sub(r'\A(?i)(subject)', '', email)   
    
    #Replace punctuation with space
    regex = re.compile('[%s]' % re.escape(string.punctuation))    
    email = regex.sub(' ', email)
    
    #Remove digits
    email = ''.join(i for i in email if not i.isdigit())
    
    #Remove consecutive characters
    email = replaceTwoOrMore(email)  

    #Convert to lower case
    email = email.lower()
    
    #Tokenize email
    unigrams = word_tokenize(email)
    
    # Read stopwords from file and tokenize them
    stopwords = open("eng_stop_lower.txt").read()
    stopwords_unigrams = word_tokenize(stopwords[:])
    
    #Remove stopwords
    unigrams = [removeStopwords(t,stopwords_unigrams) for t in unigrams]
      
    #Stemming
    unigrams = [stemmer.stem(t) for t in unigrams]

    #Rejoin words forming the email
    email = ' '.join(unigrams)
    
    #Remove additional white spaces
    email = re.sub('[\s]+', ' ', email)
    
    return email

# Look for 2 or more repetitions of character and replace with the character itself
def replaceTwoOrMore(email):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", email)

# Remove every word of the email that is listed in the stopwords vocabulary
def removeStopwords(word,stopwords_unigrams):
    for i in stopwords_unigrams:
        if word==i:
            word =''
            return word

    return word