import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer
# Print basic metrics report
from sklearn import metrics
#our module
import Email_Tools
# Import libraries
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit

def returnY(listT):
    
    listCat=[]
    
    for email, cat in listT:
        if cat == "ham":
            listCat.append("ham")
        elif cat == "spam":
            listCat.append("spam")
    return listCat
    

#Read the term frequencies of the tweets
tfTrain = Email_Tools.readFileReturnList("Train_TF.obj")
tfTest = Email_Tools.readFileReturnList("Test_TF.obj")

#Create the vectorizer
vect = DictVectorizer(sparse=True)

#Fit and transform our train data and test data
train_x=vect.fit_transform(tfTrain)
test_x=vect.fit_transform(tfTest)

#Load the tweets used for training
trainEmailsList=Email_Tools.readFileReturnList("Train_emails.obj")

#Create a list with the category of each tweet
train_y=returnY(trainEmailsList)
Email_Tools.createObjFile(train_y,'Train_Categories.obj')


#Load the tweets used for testing
testEmailsList=Email_Tools.readFileReturnList("Test_emails.obj")

#Create a list with the category of each tweet
test_y=returnY(testEmailsList)
Email_Tools.createObjFile(test_y,'Test_Categories.obj')



#Load classifier
LR = LogisticRegression()

#Train classifier
LR.fit(train_x, train_y)

# Predict for the rest
pred_y = LR.predict(test_x)
Email_Tools.createObjFile(pred_y,'LR_Pred_Categories.obj')

print "Logistic Regression metrics..."
print metrics.classification_report(test_y, pred_y)

#Accordingly for MultinomialNB
MNB=MultinomialNB(fit_prior=False)
MNB.fit(train_x, train_y)
pred_y = MNB.predict(test_x)
print "Multinomial Naive Bayes metrics..."
print metrics.classification_report(test_y, pred_y)

#Accordingly for GradientBoostingClassifier 
GB = GradientBoostingClassifier(learning_rate=0.2)
#GB requires a dense matrix but DictVectorizer produces a sparse matrix so we make x dense
train_x = train_x.todense()
GB.fit(train_x, train_y)
test_x = test_x.todense()
pred_y = GB.predict(test_x)
print "GradientBoostingClassifier metrics..."
print metrics.classification_report(test_y, pred_y)

##Accordingly for GaussianNB with dense data as required
#GNB=GaussianNB()
#train_x = train_x.todense()
#GNB.fit(train_x, train_y)
#test_x = test_x.todense()
#pred_y = GNB.predict(test_x)
#print "Gaussian Naive Bayes metrics..."
#print metrics.classification_report(test_y, pred_y)
#
##Accordingly for BernoulliNB
#BNB=BernoulliNB()
#BNB.fit(train_x, train_y)
#pred_y = BNB.predict(test_x)
#print "Bernoulli Naive Bayes metrics..."
#print metrics.classification_report(test_y, pred_y)


##Accordingly for KNeighborsClassifier 
#KNN=KNeighborsClassifier(weights='distance')
#KNN.fit(train_x, train_y)
#pred_y = KNN.predict(test_x)
#print "KNeighborsClassifier metrics..."
#print metrics.classification_report(test_y, pred_y)

##Accordingly for RandomForestClassifier 
#RFC = RandomForestClassifier(criterion='entropy', min_samples_split=6, class_weight='balanced')
#RFC.fit(train_x, train_y)
#pred_y = RFC.predict(test_x)
#print "Random Forest Classifier metrics..."
#print metrics.classification_report(test_y, pred_y)

##Accordingly for LinearSVC 
#LinearSVC = LinearSVC()
#LinearSVC.fit(train_x, train_y)
#pred_y = LinearSVC.predict(test_x)
#print "Linear SVC metrics..."
#print metrics.classification_report(test_y, pred_y)

# Define learning curves plot function
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 10), scoring='f1_macro'):

    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, 
        scoring= scoring)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

# Algorithm Dictionary
plt.gcf().clear() #cleaning the figure from previous plots
estimators = {'LR':LR,'MNB':MNB, 'GB':GB}
predictions={}

for (name,estimator) in estimators.items():
    title = "Learning Curves " + name
    predictions[name] = estimator.predict(test_x)
    # Random permutation cross-validator
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
    plot_learning_curve(estimator, title, test_x, predictions[name], (0.1, 1.01), cv=cv, n_jobs=-1)

    plt.show()
    plt.gcf().clear() #cleaning the figure from previous plots