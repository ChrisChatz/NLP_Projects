from nltk.tokenize import word_tokenize
#our module 
import Preprocessing,Tools

traintweets_list = Tools.readFileReturnList("Train_tweets.obj")


vocabularyTmp=[]
for ID,status,cat in traintweets_list:
    preprocessedStatus=Preprocessing.preprocessing(status)
    unigrams = word_tokenize(preprocessedStatus)
    for word in unigrams:
        vocabularyTmp.append(word)

#Count word frequencies
wordfreqVocabularyTmp = [vocabularyTmp.count(w) for w in vocabularyTmp]

'''replace  all  the rare words of the training subset (e.g., words that do not 
occur at least 10 times in the training subset) by a special token *rare*'''
for f in range(len(wordfreqVocabularyTmp)):
   if wordfreqVocabularyTmp[f]<10:
       vocabularyTmp[f]="*rare*"


#create vocabulary of unique words
vocabulary=[]
for word in vocabularyTmp:
    if word not in vocabulary and word!="*rare*":
        vocabulary.append(word)
        
#print vocabulary
#print len(vocabulary)
 
#Write in a file
Tools.createObjFile('Vocabulary.obj')

print "Vocabulary is created"