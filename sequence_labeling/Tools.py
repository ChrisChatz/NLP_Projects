import math
from nltk.tokenize import word_tokenize

#Implement Laplace Smoothing and create a dictionary with ngrams and their probabilities
def laplaceSmoothing(wordfreq_nMinus1grams, wordfreq_ngrams, voc):
    prob = {}
    for key, value in wordfreq_ngrams.iteritems():
        p = math.log(float(value + 1)/(wordfreq_nMinus1grams[key[0]] + voc))
        prob.update({key:p})
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