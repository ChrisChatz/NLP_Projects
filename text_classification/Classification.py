import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer
# Print basic metrics report
from sklearn import metrics
#our module
import Tools

def returnY(listT):
    
    listCat=[]
    
    for ID,stat,cat in listT:
        if cat == "negative":
            listCat.append("negative")
        elif cat == "positive":
            listCat.append("positive")
        elif cat ==  "neutral":
            listCat.append("neutral")
        
    return listCat
    

#Read the term frequencies of the tweets
tfTrain = Tools.readFileReturnList("Train_TF.obj")
tfTest = Tools.readFileReturnList("Test_TF.obj")

#Create the vectorizer
vect = DictVectorizer(sparse=True)


#Fit and transform our train data and test data
train_x=vect.fit_transform(tfTrain)
test_x=vect.fit_transform(tfTest)

#Load the tweets used for training
trainTweetsList=Tools.readFileReturnList("Train_tweets.obj")

#Create a list with the category of each tweet
train_y=returnY(trainTweetsList)

#Load the tweets used for testing
testTweetsList=Tools.readFileReturnList("Test_tweets.obj")

#Create a list with the category of each tweet
test_y=returnY(testTweetsList)


#Load classifier
LR = LogisticRegression(tol=0.0001, C=1.0, class_weight='balanced', 
                        solver='sag', max_iter=100, 
                        multi_class='ovr', verbose=3, warm_start=True, n_jobs=1)

#Train classifier
LR.fit(train_x, train_y)

print "Learning done LR!!!..."

# Predict for the rest
pred_y = LR.predict(test_x)

print metrics.classification_report(test_y, pred_y)



MNB=MultinomialNB(alpha=1.0, fit_prior=False, class_prior=None)
#Train classifier
MNB.fit(train_x, train_y)

print "Learning done MNB!!!..."

# Predict for the rest
pred_y = MNB.predict(test_x)

print metrics.classification_report(test_y, pred_y)

KNN = KNeighborsClassifier(n_neighbors=20, weights='uniform', algorithm='auto', 
                           leaf_size=30, p=2, metric='minkowski',                           
                           metric_params=None, n_jobs=1)

KNN.fit(train_x, train_y)

print "Learning done KNN!!!..."

# Predict for the rest.
pred_y = KNN.predict(test_x)


print "KNN Metrics"
print metrics.classification_report(test_y, pred_y)

#GNB = GaussianNB()
#
#train_x = train_x.todense()
#
#GNB.fit(train_x[:2000], Y_true[:2000])
#
#print "Learning done GNB!!!..."
#
## Predict for the rest.
#Y_pred = GNB.predict(train_x[2000:])
#
#
#print "GNB Metrics"
#print metrics.classification_report(Y_true[2000:], Y_pred)


#GB = GradientBoostingClassifier(loss='deviance', learning_rate=0.1, 
#                                n_estimators=100, subsample=1.0, criterion='friedman_mse', 
#                                min_samples_split=2, min_samples_leaf=1, 
#                                min_weight_fraction_leaf=0.0, 
#                                max_depth=3, min_impurity_split=1e-07, 
#                                init=None, random_state=None, max_features=None, 
#                                verbose=0, max_leaf_nodes=None, warm_start=False, 
#                                presort='auto')
#
##GB requires a dense matrix but DictVectorizer produces a sparse matrix
##So we make x dense
#train_x1 = train_x.todense()
##Train classifier
#GB.fit(train_x1[:2000], Y_true[:2000])
#
#print "Learning done GB!!!..."
#
## Predict for the rest.
#Y_pred = GB.predict(train_x1[2000:])
#
#
#print "GB Metrics"
#print metrics.classification_report(Y_true[2000:], Y_pred)



# Import libraries
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit

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
estimators = {'LR':LR,'MNB':MNB,'KNN':KNN}

for (name,estimator) in estimators.items():
    title = "Learning Curves " + name
    # Random permutation cross-validator
    cv = ShuffleSplit(n_splits=3, test_size=0.2, random_state=0)
    plot_learning_curve(estimator, title, train_x, train_y, (0.1, 1.01), cv=cv, n_jobs=-1)

    plt.show()