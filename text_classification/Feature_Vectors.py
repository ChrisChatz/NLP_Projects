from nltk.tokenize import word_tokenize
#our module 
import Preprocessing,Tools

def tfVector(status,vocabulary):
    
    unigrams = word_tokenize(status)
    tfVec={}
    for word in vocabulary:
        tfVec[word]=0
        if word in unigrams:
            tfVec[word]+=1
    for key in tfVec:
        tfVec[key]/=float(len(unigrams))
        
    return tfVec


#Read train tweets file
trainTweetsList=Tools.readFileReturnList("Train_tweets.obj")

#Read test tweets file
testTweetsList=Tools.readFileReturnList("Test_tweets.obj")

#Read vocabulary file
vocabulary=Tools.readFileReturnList("Vocabulary.obj")

#Tf for train data
vectorsTfTrain=[]
for ID,status,cat in trainTweetsList:
    preprocessedStatus=Preprocessing.preprocessing(status)
    vectorTf=tfVector(preprocessedStatus,vocabulary)
    vectorsTfTrain.append(vectorTf)

Tools.createObjFile(vectorsTfTrain,"Train_TF.obj")
print "Tf for training data ok"

#Tf for test data
vectorsTfTest=[]
for ID,status,cat in testTweetsList:
    preprocessedStatus=Preprocessing.preprocessing(status)
    vectorTf=tfVector(preprocessedStatus,vocabulary)
    vectorsTfTest.append(vectorTf)

Tools.createObjFile(vectorsTfTest,"Test_TF.obj")
print "Tf for test data ok"