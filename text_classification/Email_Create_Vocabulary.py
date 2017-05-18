from nltk.tokenize import word_tokenize
#Our modules
import Email_Preprocessing, Email_Tools

#Open the train emails file created from the Reading_Emails.py file
trainemails_list = Email_Tools.readFileReturnList("Train_emails.obj")

# Preprocess all train emails
preprocessedTrainEmails=[]
counter=0
for email, cat in trainemails_list:
    preprocessedEmail=Email_Preprocessing.preprocessing(email)
    preprocessedTrainEmails.append(preprocessedEmail)
    counter+=1
    print "Preprocessing: "+counter

Email_Tools.createObjFile(preprocessedTrainEmails,'Preprocessed_Train_Emails.obj')
print "Preprocessing of the training emails done!"

#Create a temporary vocabulary with all the words from the preprocessed train emails
vocabularyTmp=[]
for email in preprocessedTrainEmails:
    unigrams = word_tokenize(email)
    vocabularyTmp.extend(unigrams)

Email_Tools.createObjFile(vocabularyTmp,'vocabularyTmp.obj')
print "The size of the temporary vocbulary is "+len(vocabularyTmp)+" words."

# Count word frequencies in the temporary vocabulary, thus creating 
# a dictionary with all the unique words and their frequencies.
wordfreqVocabularyTmp={}
for w in vocabularyTmp:
    wordfreqVocabularyTmp[w] = vocabularyTmp.count(w)

Email_Tools.createObjFile(wordfreqVocabularyTmp,'wordfreqVocabularyTmp.obj')
print "Word frequencies for the temporary vocabulary found."

# Keep in the final vocabulary the words that occur at least 10 times in the training subset  
vocabulary=[]
for word, frequency in wordfreqVocabularyTmp.iteritems():
    if frequency>=10:
        vocabulary.append(word)

Email_Tools.createObjFile(vocabulary,'Emails_Vocabulary.obj')
print "Final vocabulary is created."