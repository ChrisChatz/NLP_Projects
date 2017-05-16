import math
from nltk.tokenize import word_tokenize

def vocabulary(ngram):
    vocabulary=[]
    for word in ngram:
        if word not in vocabulary:
            vocabulary.append(word)
    return vocabulary

def laplaceSmoothing(bigrams, freqUn, voc):
    prob = {}
    i=0
    for key in bigrams:
        p = math.log(float((bigrams[key] + 1))/(freqUn[i] + voc))
        i+=1
        prob[key]=p

    return prob

def countWords(unigrams1,unigrams2):
    counter=0
    for i in range(len(unigrams1)):
        if str(unigrams1[i])==str(unigrams2[i]):
            counter+=1
    return counter
            
def compareSentences(testSentence,errorSentence,correctedSentence):

    unigramsTest=word_tokenize(testSentence)
    unigramsError=word_tokenize(errorSentence)
    unigramsCorrected=word_tokenize(correctedSentence)
    counter1=0
    for i in range(len(unigramsTest)):
        if str(unigramsTest[i])!=str(unigramsError[i]):
            counter1+=1
    counter2=0
    for i in range(len(unigramsTest)):
        if str(unigramsTest[i])==str(unigramsCorrected[i]) and str(unigramsTest[i])!=str(unigramsError[i]):
            counter2+=1
            
   
    print "The correction is %s per cent" % (100 * counter2/float(counter1))