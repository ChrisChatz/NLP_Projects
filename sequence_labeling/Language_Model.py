from nltk.corpus import europarl_raw
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import ngrams
import Tools

def probabilitiesAndVoc():
    
    #Read the data
    training_data=europarl_raw.english.raw('europarl-v7.el-en.en')
    
    #Select the first 200000 characters and split them to sentences
    sentences=[sent for sent in sent_tokenize(training_data[:400000])]
    newSentences=[]
    for s in sentences:
        s="start1 "+s
        newSentences.append(s)
    
    unigrams = [word_tokenize(sentence) for sentence in newSentences]
    unigrams=sum(unigrams,[]) 
  
    # Count unigrams frequencies, thus creating 
    # a dictionary with all the unique words and their frequencies.
    wordfreq_unigrams={}
    for u in unigrams:
        wordfreq_unigrams[u] = unigrams.count(u)
    
    
    '''replace  all  the rare words of the training subset (e.g., words that do not 
    occur at least 2 times in the training subset) by a special token *rare*'''
    frequent_unigrams={}
    counter=0
    for key, value in wordfreq_unigrams.iteritems():
        if value<2:
            unigrams[counter]="*rare*"
            counter+=1
        else:
            frequent_unigrams.update({key:value})
            counter+=1
             
    #Count all the unique frequent unigrams
    voc_uni = len(frequent_unigrams)
    
    bigrams = ngrams(unigrams,2)
    
    #Keep all the bigrams that consist of non rare unigrams
    frequent_bigrams=[]
    for x,y in bigrams:
        if x!="*rare*" and y!="*rare*":
            if frequent_bigrams == [] and x!="start1": #if the first word of the corpus was *rare*
                frequent_bigrams.append(("start1",x))
                frequent_bigrams.append((x,y))
            else:
                frequent_bigrams.append((x,y))
                
    
    # Count bigrams frequencies, thus creating 
    # a dictionary with all the unique bigrams and their frequencies.
    wordfreq_bigrams={}
    for x,y in frequent_bigrams:
        wordfreq_bigrams[(x,y)] = frequent_bigrams.count((x,y))
    
    
#    laplace_bigrams=Tools.laplaceSmoothing(bigramsDict,wordfreq_vunigrams,voc_len)
    laplace_bigrams=Tools.laplaceSmoothing(wordfreq_unigrams,wordfreq_bigrams,voc_uni)
    voc=list(frequent_unigrams.keys())
    
    return laplace_bigrams,voc