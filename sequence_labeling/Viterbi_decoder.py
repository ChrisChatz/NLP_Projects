from nltk.tokenize import word_tokenize
import math
import Distances,Language_Model

#Take as an input the wrong word and returns the 5 closest ones with respect to levenshtein distance
def minDistance(word,voc,endList):
 
    tmpList=[]
    
    for i in voc:
        tmpList.append(Distances.levenshtein_Distance(word,i))
    tmpList=sorted(tmpList)
    return tmpList[:endList]
        


test_sentence="start0 start1 I declar."


prob,voc=Language_Model.probabilitiesAndVoc()


unigrams = word_tokenize(test_sentence)

V = [{}]
wordsDict={}
prevBigram=[]
prevBigram.append((0,(unigrams[0],unigrams[1])))
V[0][unigrams[0],unigrams[1]]={"prob":0.0}
wordsDict[(unigrams[2],1)]=minDistance(unigrams[2],voc,5)

#Those for loops are for step one
for un,lvl in wordsDict.keys():
    V.append({})
    for dist,word in wordsDict[(un,lvl)]: 
        levenshtein=math.log(1/float((dist+1)))
        for z,(x,y) in prevBigram:
            if z==0:
                    try:
                        V[1][y,word] = {"prob":levenshtein + prob[(unigrams[1],word)]}
                    except:
                        V[1][y,word] = {"prob":levenshtein + math.log(1/float(len(voc)))}
        prevBigram.append((1,(unigrams[1],word)))

#Those for loops are for step 2 and so on
for step in range(3, len(unigrams)):

        V.append({})
        wordsDict[(unigrams[step],step-1)]=minDistance(unigrams[step],voc,5)
        for un,lvl in wordsDict.keys():
            if lvl==step-1:
                for z,(x,y) in prevBigram:
                    if z==step-2:
                        #take the max probability from the previous step
                        max_prob=max(V[step-2][x,y].values())
                        for dist,word in wordsDict[(un,lvl)]:
                            levenshtein=math.log(1/float((dist+1)))
                            
                            try:
                                V[step-1][y,word]={"prob":levenshtein + prob[(y,word)] + max_prob}
                            except:
                                V[step-1][y,word]={"prob":levenshtein + math.log(1/float(len(voc)))+ max_prob}
                            w=step-1  
                            if (w,(y,word)) not in prevBigram:
                                prevBigram.append((step-1,(y,word)))
                    

for vit in V:
    print max(vit)

