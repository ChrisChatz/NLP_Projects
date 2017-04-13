# -*- coding: utf-8 -*-

from nltk.tokenize import word_tokenize
import math
import pickle 


def tfVector(status,vocabulary):
    unigrams = word_tokenize(status.lower())
    tfVec={}
    for word in vocabulary:
        tfVec[word]=0
        if word in unigrams:
            tfVec[word]+=1
    for key in tfVec:
        tfVec[key]/=float(len(unigrams))
        
    return tfVec

twitterTrainFile = open("Train_tweets.obj", 'rb') 
traintweets_list = pickle.load(twitterTrainFile)
twitterTrainFile.close()

twitterVoc = open("Vocabulary.obj", 'rb') 
vocabulary = pickle.load(twitterVoc)
twitterVoc.close()

NumberOfDocuments=0
for tweet in traintweets_list:
    NumberOfDocuments+=1

vectors_tf_list=[]
for ID,status,cat in traintweets_list:
    vectorTf=tfVector(status,vocabulary)
    vectors_tf_list.append(vectorTf)

object_pi_1=vectors_tf_list
file_pi_1 = open('TF_tweets.obj', 'w') 
pickle.dump(object_pi_1, file_pi_1) 
file_pi_1.close()

print "TF vector is created"
