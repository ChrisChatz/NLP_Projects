from nltk.tokenize import word_tokenize
# Our module
import Email_Tools

# Select the words with the higher information gain by appending to
# the final list only those that appear in more than 3 emails.
def selection(emails, voc):
    IG ={}
    selected_features=[]
    for word in voc:
        IG[word]=0
        for email in emails:
            unigrams = word_tokenize(email)
            if word in unigrams:
                IG[word]+=1
                if IG[word]>3:
                    selected_features.append(word)
                    break
    return selected_features

#Read the vocabulary file
voc = Email_Tools.readFileReturnList("Emails_Vocabulary.obj")

#Read the preprocessed train emails
preprocessedTrainEmails = Email_Tools.readFileReturnList("Preprocessed_Train_Emails.obj")
       
#Select the features with the higher information gain
final_features = selection(preprocessedTrainEmails, voc)    
print "Features selected!"
Email_Tools.createObjFile(final_features,'Emails_Selected_Vocabulary.obj')