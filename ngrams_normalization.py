# -*- coding: utf-8 -*-

from nltk.corpus import europarl_raw
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

def CheckLogProb(sentence,valid_bigrams,Laplace_bigrams,voc_uni,valid_trigrams,
                 Laplace_trigrams,voc_bi):
    sentence = sentence.lower()
    unigrams=word_tokenize(sentence)
    test_bigrams = ngrams(["$start1"]+unigrams,2)
    test_trigrams =ngrams(["$start1","$start2"]+unigrams,3)

    valid_tbigrams=[]
    for x,y in test_bigrams:
        valid_tbigrams.append((x,y))
    
    valid_ttrigrams=[]
    for x,y,z in test_trigrams:
        valid_ttrigrams.append((x,y,z))

    bigramsLogProb=LogProbabilities(valid_bigrams,valid_tbigrams,
                                    Laplace_bigrams,voc_uni)
    trigramsLogProb=LogProbabilities(valid_trigrams,valid_ttrigrams,
                                     Laplace_trigrams,voc_bi)
    
    return bigramsLogProb,trigramsLogProb

    

def LogProbabilities(ngrams,tngrams,Laplace_ngrams,voc):
    sumProb=0
    for i in range(len(ngrams)):
        if ngrams[i] in tngrams:
            sumProb+=math.log(Laplace_ngrams[i])
        else:
            sumProb+=math.log(float(1)/voc)
        
    return sumProb
    
   
training_data=europarl_raw.english.raw('europarl-v7.el-en.en')
training_data = training_data.lower()
unigrams = word_tokenize(training_data[0:200000])
wordfreq_unigrams = [unigrams.count(w) for w in unigrams]

'''replace  all  the rare words of the training subset (e.g., words that do not 
occur at least 10 times in the training subset) by a special token *rare*'''
for f in range(len(wordfreq_unigrams)):
   if wordfreq_unigrams[f]<10:
       unigrams[f]="*rare*"


valid_unigrams=[]
for w in range(len(unigrams)):
    if unigrams[w]!="*rare*":
        valid_unigrams.append(unigrams[w])    
    
wordfreq_vunigrams=[valid_unigrams.count(w) for w in valid_unigrams]

#do Laplace smoothing in our bigrams model
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


Laplace_bigrams=LaplaceSmoothing(valid_unigrams,valid_bigrams,wordfreq_vunigrams,
                       wordfreq_vbigrams,voc_uni)

#do Laplace smoothing in our trigrams model
trigrams = ngrams(["$start1","$start2"]+unigrams,3)
valid_trigrams=[]
for x,y,z in trigrams:
    if x!="*rare*" and y!="*rare*" and z!="*rare*":
        if valid_trigrams==[] and x!="$start1":
            valid_trigrams.append(("$start1","$start2",x))
            valid_trigrams.append(("$start2",x,y))
            valid_trigrams.append((x,y,z))
        else:
            valid_trigrams.append((x,y,z))

wordfreq_vtrigrams = [valid_trigrams.count(w) for w in valid_trigrams]

voc_bi=vocabulary(valid_bigrams)

Laplace_trigrams=LaplaceSmoothing(valid_bigrams,valid_trigrams,wordfreq_vbigrams,
                       wordfreq_vtrigrams,voc_bi)


''' Check the log-probabilities that our trained models return when given 
(correct) sentences from the test subset vs. (incorrect) sentences of 
the  same  length  (in  words)  consisting  of  randomly  selected vocabulary 
words''' 

correct_sentence="You have requested a debate on this subject in the course of the next few days, during this part-session."
correct_log_Prob=CheckLogProb(correct_sentence,valid_bigrams,Laplace_bigrams,
                              voc_uni,valid_trigrams,Laplace_trigrams,voc_bi)

print "Log-probability of correct sentence: %s" %(correct_log_Prob,)

incorrect_sentence="This is is is is is is is is is is is is is is is is is is is is."
incorrect_log_Prob=CheckLogProb(incorrect_sentence,valid_bigrams,
                                Laplace_bigrams,voc_uni,valid_trigrams,
                                Laplace_trigrams,voc_bi)

print "Log-probability of incorrect sentence:%s" %(incorrect_log_Prob,)


#Predict the next (vocabulary) word, as in a predictive keyboard

#Bigram predictions
word = 'is'
bigram_word_predictions = []

counter = 0
for x,y in valid_bigrams:
    if word == x and y not in bigram_word_predictions:
        bigram_word_predictions.append((y,Laplace_bigrams[counter]))
    counter+= 1

bigram_word_predictions.sort(key=operator.itemgetter(1), reverse=True)
print "Predict bigram: {0}".format(bigram_word_predictions[0:3])

#Trigram predictions
word1='it'
word2='is'
trigram_word_predictions = []    
counter = 0
for x,y,z in valid_trigrams:
    if word1 == x and word2==y :
        trigram_word_predictions.append((z,Laplace_trigrams[counter]))
    counter+= 1

trigram_word_predictions.sort(key=operator.itemgetter(1), reverse=True)
print "Predict trigram: {0}".format(trigram_word_predictions[0:3])


'''Estimate  the  language  cross-entropy  and  perplexity  of  our  models  on
the test subset  of  the corpus. '''

test_data=europarl_raw.english.raw('europarl-v7.el-en.en')
test_data = test_data.lower()        
test_unigrams = word_tokenize(test_data[200001:208001])
test_bigrams = ngrams(["$start1"]+unigrams,2)
test_trigrams =ngrams(["$start1","$start2"]+unigrams,3)

valid_tbigrams=[]
for x,y in test_bigrams:
    valid_tbigrams.append((x,y))
    
valid_ttrigrams=[]
for x,y,z in test_trigrams:
    valid_ttrigrams.append((x,y,z))

bigramsLogProb=LogProbabilities(valid_bigrams,valid_tbigrams,Laplace_bigrams,voc_uni)
trigramsLogProb=LogProbabilities(valid_trigrams,valid_ttrigrams,Laplace_trigrams,voc_bi)
    
cross_entropy_bigrams=-(1/float(len(valid_tbigrams)))*bigramsLogProb
cross_entropy_trigrams=-(1/float(len(valid_ttrigrams)))*trigramsLogProb
                        
print "Cross-entropy of bigrams: "+str(cross_entropy_bigrams)
print "Cross-entropy of trigrams: "+str(cross_entropy_trigrams)

perplexity_bigrams = math.pow(2,cross_entropy_bigrams)
perplexity_trigrams = math.pow(2,cross_entropy_trigrams)

print "Perplexity of bigrams: "+str(perplexity_bigrams)
print "Perplexity of trigrams: "+str(perplexity_trigrams)