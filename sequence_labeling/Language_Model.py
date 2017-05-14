from nltk.corpus import europarl_raw
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import ngrams
import Tools

def probabilitiesAndVoc():
    training_data=europarl_raw.english.raw('europarl-v7.el-en.en')
    sentences=[sent for sent in sent_tokenize(training_data[0:400000])]
    newSentences=[]
    for s in sentences:
        s="start1 "+s
        newSentences.append(s)
        
    unigrams = [word_tokenize(sentence) for sentence in newSentences]
    unigrams=sum(unigrams,[]) 
    
    wordfreq_unigrams = [unigrams.count(w) for w in unigrams]
    
    #print len(unigrams)
    '''replace  all  the rare words of the training subset (e.g., words that do not 
    occur at least 10 times in the training subset) by a special token *rare*'''
    for f in range(len(wordfreq_unigrams)):
       if wordfreq_unigrams[f]<10 or unigrams[f]=="start1":
           unigrams[f]="*rare*"
    
    
    valid_unigrams=[]
    for w in range(len(unigrams)):
        if unigrams[w]!="*rare*":
            valid_unigrams.append(str(unigrams[w]))
            
               
    wordfreq_vunigrams=[valid_unigrams.count(w) for w in valid_unigrams]
    
    #do Laplace smoothing in our bigrams model
    voc=Tools.vocabulary(valid_unigrams)
    voc_len = len(voc)
    
    bigrams = ngrams(unigrams,2)
    valid_bigrams=[]
    for x,y in bigrams:
        if x!="*rare*" and y!="*rare*":
            valid_bigrams.append((str(x),str(y)))
    
    bigramsFreq=[valid_bigrams.count(w) for w in valid_bigrams]
    bigramsDict={}
    i=0
    for bigram in valid_bigrams:
        bigramsDict[bigram]=bigramsFreq[i]
        i+=1

    
    laplace_bigrams=Tools.laplaceSmoothing(bigramsDict,wordfreq_vunigrams,voc_len)

    
    return laplace_bigrams,voc