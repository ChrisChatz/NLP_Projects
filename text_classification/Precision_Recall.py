import Email_Tools
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import ShuffleSplit


def gianadoume(estimator,test_y_ham, pred_y_ham, test_y_spam, pred_y_spam):
    
    precision = {}
    recall = {}
    precision["ham"], recall["ham"], _ = precision_recall_curve(test_y_ham, pred_y_ham)
    precision["spam"], recall["spam"], _ = precision_recall_curve(test_y_spam, pred_y_spam)
    plt.clf()
    for i, color in zip(["ham","spam"], ['red','green']):
        plt.plot(recall[i], precision[i], color=color,label='Precision-recall curve of class {0}'.format(i))
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend(loc="lower right")
    return plt

trainEmailsList=Email_Tools.readFileReturnList("Train_emails.obj")
preTestEmails=Email_Tools.readFileReturnList("Preprocessed_Test_Emails.obj")
trainCategories=Email_Tools.readFileReturnList("Train_Categories.obj")
testCategories=Email_Tools.readFileReturnList("Test_Categories.obj")
LRPredCategories=Email_Tools.readFileReturnList("LR_Pred_Categories.obj")

tfTrain = Email_Tools.readFileReturnList("Train_TF.obj")
tfTest = Email_Tools.readFileReturnList("Test_TF.obj")

#Create two list of the vectors for the ham and spam categories of test emails, separately
tfTest_ham=[]
tfTest_spam=[]
test_y_ham = []
test_y_spam = []

for i in range(len(tfTest)):
    if testCategories[i]=="ham":
        tfTest_ham.append(tfTest[i])
        test_y_ham.append("ham")
    else:
        tfTest_spam.append(tfTest[i])
        test_y_spam.append("spam")

vect = DictVectorizer(sparse=True)

train_x = vect.fit_transform(tfTrain)
train_y = trainCategories

LR = LogisticRegression()
LR.fit(train_x, train_y)

test_x_ham=vect.fit_transform(tfTest_ham)
test_x_spam=vect.fit_transform(tfTest_spam)


pred_y_ham = LR.predict(test_x_ham)
pred_y_spam = LR.predict(test_x_spam)

# pred_y = label_binarize(pred_y, classes=range(2)) den kanei swsto binarization.. why???????!
new_pred_y_ham=[]
for y in pred_y_ham:
    if y=='spam':
        y=0
        new_pred_y_ham.append(y)
    else:
        y=1
        new_pred_y_ham.append(y)

new_pred_y_spam=[]
for y in pred_y_spam:
    if y=='spam':
        y=0
        new_pred_y_spam.append(y)
    else:
        y=1
        new_pred_y_spam.append(y)    
        
new_test_y_ham=[]
for y in test_y_ham:
    if y=='spam':
        y=0
        new_test_y_ham.append(y)
    else:
        y=1
        new_test_y_ham.append(y)

new_test_y_spam=[]
for y in test_y_spam:
    if y=='spam':
        y=0
        new_test_y_spam.append(y)
    else:
        y=1
        new_test_y_spam.append(y)

plt2 = gianadoume(LR, new_test_y_ham, new_pred_y_ham, new_test_y_spam, new_pred_y_spam)
plt2.show()
plt2.close()



