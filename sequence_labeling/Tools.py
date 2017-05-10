import math

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