from nltk.tokenize import word_tokenize
import math
import Distances

#Take as an input the wrong word and returns the 5 closest ones with respect to levenshtein distance
def minDistance(word,voc,endList):
 
    punctuationList=['.',',','-','(',')','?','/',':','%','"',"'"]
    tmpList=[]
    letters1=list(word)
    if word.isdigit():
        tmpList.append((0,word))
        return tmpList
    
    elif word not in punctuationList:
        for i in voc:
            if i not in punctuationList:
                letters2=list(i)
        #        Check if the first letter is upper to compare it with specific words
                if letters1[0].isupper() and letters2[0].isupper():
                    tmpList.append(Distances.levenshtein_Distance(word,i))
                elif letters1[0].islower() and letters2[0].islower():
                    tmpList.append(Distances.levenshtein_Distance(word,i))
                elif letters1[0] in punctuationList:
                    tmpList.append(Distances.levenshtein_Distance("".join(letters1[1:-1]),i))
        tmpList=sorted(tmpList)
        return tmpList[:endList]
    else:
        tmpList.append((0,word))
        return tmpList
        

def viterbiAlgorithm(testSentence,prob,voc):
    
    testSentence="start0 start1 "+testSentence
    unigrams = word_tokenize(testSentence)
    
    #list of dictionaries    
    V = [{}]
    wordsDict={}
    prevBigram=[]
    prevBigram.append((0,(str(unigrams[0]),str(unigrams[1]))))
    V[0][unigrams[0],unigrams[1]]={"prob":0.0, "previous":None}
    wordsDict[(unigrams[2],1)]=minDistance(str(unigrams[2]),voc,5)
#    print wordsDict
    
    #Those for loops are for step one
    for un,lvl in wordsDict.keys():
        V.append({})
        for dist,word in wordsDict[(un,lvl)]: 
            levenshtein=math.log(1/float((dist+1)))
            for z,(x,y) in prevBigram:
                if z==0:
                        try:
                            V[1][y,word] = {"prob":levenshtein + prob[(str(unigrams[1]),word)], "previous":(x,y)}
                        except:
                            V[1][y,word] = {"prob":levenshtein + math.log(1/float(len(voc))), "previous":(x,y)}
            prevBigram.append((1,(unigrams[1],word)))
    
    #Those for loops are for step 2 and so on
    for step in range(3, len(unigrams)):
    
            V.append({})
            wordsDict[(unigrams[step],step-1)]=minDistance(str(unigrams[step]),voc,5)
#            print wordsDict
            for un,lvl in wordsDict.keys():
                if lvl==step-1:
                    for z,(x,y) in prevBigram:
                        if z==step-2:
                            for dist,word in wordsDict[(un,lvl)]:
                                #take the max probability from the previous step
                                try:
                                    max_prob = max(value["prob"]+prob[(y,word)] for value in V[step-2].values())
                                except:
                                    max_prob = max(value["prob"]+ math.log(1/float(len(voc))) for value in V[step-2].values())
                                levenshtein=math.log(1/float((dist+1)))
                                V[step-1][y,word]={"prob":levenshtein + max_prob, "previous":(x,y)}
                                w=step-1  
                                if (w,(y,word)) not in prevBigram:
                                    prevBigram.append((step-1,(y,word)))
                        
    
    opt = []   
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
    
        if data["prob"] == max_prob:
    
            opt.append(st)
    
            previous = st
    
            break
    
    
    # Follow the backtrack till the first observation
    
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["previous"])
        previous = V[t + 1][previous]["previous"]
    
    
    correctedSentenceList=[]
    for first,second in opt:
        if second=="start1":
            continue
        correctedSentenceList.append(second)
        
    correctedSentence=" ".join(correctedSentenceList)
    return correctedSentence