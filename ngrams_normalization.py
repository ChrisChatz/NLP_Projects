# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from nltk.corpus import europarl_raw
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk import ngrams
import math
import operator


def vocabulary(ngram):
    Vocabulary=0
    unique_words = set(ngram)
    for word in unique_words:
        Vocabulary=Vocabulary+1
    return Vocabulary

def LaplaceSmoothing(list1, list2, freq1, freq2, voc):
    prob = []
    for i in range(len(list2)):
        p = float((freq2[i] + 1))/(freq1[i] + voc)
        prob.append(p)

    return prob

def LogProbabilities(ngrams,tngrams,Laplace_ngrams,voc):
    sumProb=0
    for i in range(len(tngrams)):
        if tngrams[i] in ngrams:
            sumProb+=math.log(Laplace_ngrams[i])
        else:
            sumProb+=math.log(float(1)/voc)
        
    return sumProb
    
   
training_data=europarl_raw.english.raw('europarl-v7.el-en.en')
unigrams = word_tokenize(training_data[0:200000])



wordfreq_unigrams = [unigrams.count(w) for w in unigrams]

for f in range(len(wordfreq_unigrams)):
   if wordfreq_unigrams[f]<10:
       unigrams[f]="*rare*"


valid_unigrams=[]
for w in range(len(unigrams)):
    if unigrams[w]!="*rare*":
        valid_unigrams.append(unigrams[w])    
    
wordfreq_vunigrams=[valid_unigrams.count(w) for w in valid_unigrams]

voc_uni = vocabulary(valid_unigrams)

bigrams = ngrams(["$start1"]+unigrams,2)
valid_bigrams=[]
for x,y in bigrams:
    if x!="*rare*" and y!="*rare*":
        if valid_bigrams == [] and x!="$start1":
            valid_bigrams.append(("$start1",x))
            valid_bigrams.append((x,y))
        else:
            valid_bigrams.append((x,y))

wordfreq_vbigrams = [valid_bigrams.count(w) for w in valid_bigrams]
#print wordfreq_vbigrams 
#print valid_bigrams

Laplace_bigrams=LaplaceSmoothing(valid_unigrams,valid_bigrams,wordfreq_vunigrams,
                       wordfreq_vbigrams,voc_uni)

#trigrams = ngrams(["$start1","$start2"]+unigrams,3)
#valid_trigrams=[]
#for x,y,z in trigrams:
#    if x!="*rare*" and y!="*rare*" and z!="*rare*":
#        if valid_trigrams==[] and x!="$start1":
#            valid_trigrams.append(("$start1","$start2",x))
#            valid_trigrams.append(("$start2",x,y))
#            valid_trigrams.append((x,y,z))
#        else:
#            valid_trigrams.append((x,y,z))
#
#wordfreq_vtrigrams = [valid_trigrams.count(w) for w in valid_trigrams]
##print wordfreq_vtrigrams     
##print valid_trigrams
#
#voc_bi=vocabulary(valid_bigrams)
#
#Laplace_trigrams=LaplaceSmoothing(valid_bigrams,valid_trigrams,wordfreq_vbigrams,
#                       wordfreq_vtrigrams,voc_bi)




##test_data=europarl_raw.english.raw('ep-00-02-17.en')
#test_data=gutenberg.raw('melville-moby_dick.txt')
#test_unigrams = word_tokenize(test_data[0:20000])
#test_bigrams = ngrams(["$start1"]+test_unigrams,2)
#test_trigrams =ngrams(["$start1","$start2"]+test_unigrams,3)
#
#valid_tbigrams=[]
#for x,y in test_bigrams:
#    valid_tbigrams.append((x,y))
#    
#valid_ttrigrams=[]
#for x,y,z in test_trigrams:
#    valid_ttrigrams.append((x,y,z))
#
#
#
#bigramsLogProb=LogProbabilities(valid_bigrams,valid_tbigrams,Laplace_bigrams,voc_uni)
#trigramsLogProb=LogProbabilities(valid_trigrams,valid_ttrigrams,Laplace_trigrams,voc_bi)

#print bigramsLogProb
#print trigramsLogProb

#Bigram predictions

word = 'is'
bigram_word_predictions = []

counter = 0
for x,y in valid_bigrams:
    if word == x and y not in bigram_word_predictions:
        bigram_word_predictions.append((y,Laplace_bigrams[counter]))
    counter+= 1

bigram_word_predictions.sort(key=operator.itemgetter(1), reverse=True)
print bigram_word_predictions[0:3]

##Trigram predictions
#word1='it'
#word2='is'
#trigram_word_predictions = []    
#counter = 0
#for x,y,z in valid_trigrams:
#    if word1 == x and word2==y :
#        trigram_word_predictions.append((z,Laplace_trigrams[counter]))
#    counter+= 1
#
#trigram_word_predictions.sort(key=operator.itemgetter(1), reverse=True)
#print trigram_word_predictions[0:3]


##cross entropy and perplexity
#cross_entropy_bigrams=-(1/float(len(valid_tbigrams)))*bigramsLogProb
#cross_entropy_trigrams=-(1/float(len(valid_ttrigrams)))*trigramsLogProb
#                        
#print cross_entropy_bigrams
#print cross_entropy_trigrams
#
#
#perplexity_bigrams = math.pow(2,cross_entropy_bigrams)
#perplexity_trigrams = math.pow(2,cross_entropy_trigrams)
#
#print perplexity_bigrams
#print perplexity_trigrams