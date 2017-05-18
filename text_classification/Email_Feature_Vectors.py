from nltk.tokenize import word_tokenize
#Our modules
import Email_Preprocessing, Email_Tools

# Count how many times each word of our vocabulary exists in each email
# thus creating the term-frequency vector for the email
def tfVector(email,vocabulary):
    unigrams = word_tokenize(email)
    tfVec={}
    for word in vocabulary:
        tfVec[word]=0
        if word in unigrams:
            tfVec[word]=email.count(word)
        
    return tfVec

#Read the vocabulary created after feature selection
vocabulary=Email_Tools.readFileReturnList("Emails_Selected_Vocabulary.obj")

#Create tf vectors for train data
vectorsTfTrain=[]
preprocessedTrainEmails = Email_Tools.readFileReturnList("Preprocessed_Train_Emails.obj")

counter=0
for preprocessedEmail in preprocessedTrainEmails:
    vectorTf=tfVector(preprocessedEmail,vocabulary)
    vectorsTfTrain.append(vectorTf)
    counter+=1
    print counter+'-train tf'

Email_Tools.createObjFile(vectorsTfTrain,"Train_TF2.obj")
print "Tf vectors for training data created!"

# Read the test emails file created from the Reading_Emails.py file
trainemails_list = Email_Tools.readFileReturnList("Test_emails.obj")

# Preprocess all test emails
preprocessedTestEmails=[]
counter=0
for email in trainemails_list:
    preprocessedEmail=Email_Preprocessing.preprocessing(email)
    preprocessedTestEmails.append(preprocessedEmail)
    counter+=1
    print "Preprocessing: "+counter

Email_Tools.createObjFile(preprocessedTestEmails,'Preprocessed_Test_Emails.obj')
print "Preprocessing of the test emails done!"

#Create tf vectors for test data
vectorsTfTest=[]

counter=0
for preprocessedEmail in preprocessedTestEmails:
    vectorTf=tfVector(preprocessedEmail,vocabulary)
    vectorsTfTest.append(vectorTf)
    counter+=1
    print counter+'-test tf'

Email_Tools.createObjFile(vectorsTfTest,"Test_TF2.obj")
print "Tf vectors for test data created!"