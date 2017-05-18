import os
import re
#our module
import Email_Tools

#In a chosen directory, we open all email files, detect the category (spam/ham)
# given in the file name and append the content and category to a list.
def createListOfEmails(filenames, directory):
    list=[]
    counter = 0
    spamc = 0
    hamc = 0
    for filename in filenames:
        counter+=1
        emailFile = open(directory+filename, "r")
        data = emailFile.read()
        if (pattern.match(filename)):
            list.append((data,'spam'))
            spamc+=1
        else:
            list.append((data,'ham'))
            hamc+=1
        emailFile.close()
    print "Total: ", counter
    print "Spam: ",spamc
    print "Ham: ",hamc
    return list

#Defining regex pattern for detecting email category (spam/ham) according to filename
pattern = re.compile("spmsg.*")

print "\nReading train emails..."
trainDir = 'Email_Datasets/lingspam_public/bare/train/'
filenames = os.listdir(trainDir)
emails_train_list = createListOfEmails(filenames, trainDir)
Email_Tools.createObjFile(emails_train_list,'Train_emails.obj')
print "Reading done!!!!\n"

print "Reading test emails..."
testDir = 'Email_Datasets/lingspam_public/bare/test/'
filenames = os.listdir(testDir)
emails_test_list = createListOfEmails(filenames, testDir)
Email_Tools.createObjFile(emails_test_list,'Test_emails.obj')
print "Reading done!!!!"