from nltk.tokenize import word_tokenize
import random

def randomSpellingErrors(sentence):
    chars=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','w','v','x','y','z']
    unigrams=word_tokenize(sentence)
    errorList=[]
    for word in unigrams:
        errorWord=word
        error=random.randint(1,100)
        indexRand=random.randint(0,(len(word)-1))
        charRand=random.randint(0,25)
        
        if len(word)>=2 and len(word)<=3 and error>80:
            errorWord=word[:indexRand]+chars[charRand]+word[indexRand+1:]
        elif len(word)>=4 and len(word)<=5 and error>70:
            errorWord=word[:indexRand]+chars[charRand]+word[indexRand+1:]
        elif len(word)>=4 and len(word)<=5 and error>60:
            errorWord=word[:indexRand]+word[indexRand+1:]
        elif len(word)>=6 and len(word)<=7 and error>60:
            errorWord=word[:indexRand]+chars[charRand]+word[indexRand+1:]
        elif len(word)>=6 and len(word)<=7 and error>40:
            errorWord=word[:indexRand]+word[indexRand+1:]
        elif len(word)>=8 and len(word)<=12 and error>40:
            errorWord=word[:indexRand]+chars[charRand]+word[indexRand+1:]
        
        errorList.append(errorWord)
    errorSent=" ".join(errorList)   
        
    return errorSent  