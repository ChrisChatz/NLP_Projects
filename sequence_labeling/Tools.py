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


def compareSentences(testSentence,correctedSentence):

    unigramsTest=word_tokenize(testSentence)
    unigramsCorrected=word_tokenize(correctedSentence)
    counter=0
    for i in range(len(unigramsTest)):
        if str(unigramsTest)==str(unigramsCorrected):
            counter+=1
            
    print "The correction is %s per cent" % (100 * counter/float((len(testSentence))))