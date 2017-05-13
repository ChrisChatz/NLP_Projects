from nltk.corpus import europarl_raw
from nltk.tokenize import sent_tokenize
import Random_Spelling_Errors,Viterbi_decoder,Language_Model


#load probabilities of bigram model and vocabulary from training data
print "Train language model"
prob,voc=Language_Model.probabilitiesAndVoc()
print "Training done"
print "------------------------------------------------------------------------------"

test_data=europarl_raw.english.raw('europarl-v7.el-en.en')

sentences=[sent for sent in sent_tokenize(test_data[0:3000])]
newSentences=[]
for s in sentences:
    newSentences.append(s)

for sent in newSentences:
    print "Test Sentence:  %s" %sent
    #Introduce random spelling errors in test dataset
    testSentences=Random_Spelling_Errors.randomSpellingErrors(sent)
    print "Error Sentence:  %s" %testSentences
    #Call viterbi decoder to correct spelling errors
    correctedSentence=Viterbi_decoder.viterbiAlgorithm(testSentences,prob,voc)
    print "Corrected Sentence:  %s" %correctedSentence
    print "--------------------------------------------------------------------------"
