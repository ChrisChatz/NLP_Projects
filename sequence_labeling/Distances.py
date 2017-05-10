def levenshtein_Distance(word1,word2):
    
    word1="#"+word1
    wordTmp="#"+word2
    letters1 = list(word1)
    letters2 = list(wordTmp)
    
    # Initializing table
    table = [ [0 for i in range(len(word1))] for j in range(len(wordTmp))]
    
    for i in range (len(word1)):
        table[0][i] = i
    
    for j in range (len(wordTmp)):
        table[j][0] = j
    
    
    for i in range (1,len(word1)):
        
        for j in range (1,len(wordTmp)):
            tmpList=[]
            x = table[j][i-1]+1
            tmpList.append(x)
            y = table[j-1][i]+1
            tmpList.append(y)
            if letters1[i] == letters2[j]:
                z = table[j-1][i-1]
            else:
                z = table[j-1][i-1]+2
              
            tmpList.append(z) 
            table[j][i] =min(tmpList)
    
    
    return table[-1][-1],word2