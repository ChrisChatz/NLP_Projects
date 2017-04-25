import twitter

#our module 
import Tools


def createListOfTweets(twitterFile):
    data = twitterFile.readlines()
    tweets_list = []
    NumberOfDocuments=0
    for line in data:
        tweet = line.split()
        try:
            status = api.GetStatus(status_id = tweet[0])
            tweets_list.append((tweet[0], status.text, tweet[1]))
            NumberOfDocuments+=1
            print NumberOfDocuments
        except:
            continue
        
    return tweets_list
    
    
#Setting up Twitter API
api = twitter.Api(
 consumer_key='...',
 consumer_secret='...',
 access_token_key='...',
 access_token_secret='...'
 )

#Training Tweets
twitterTrainFile = open("100_topics_100_tweets.sentence-three-point.subtask-A.train.gold.txt", "r")
trainTweetsList=createListOfTweets(twitterTrainFile)
twitterTrainFile.close()

Tools.createObjFile(trainTweetsList,'Train_tweets.obj')
print "Reading of train tweets finish!!!!"

#Testing Tweets
twitterTestFile = open("100_topics_100_tweets.sentence-three-point.subtask-A.devtest.gold.txt", "r")
testTweetsList=createListOfTweets(twitterTestFile)
twitterTestFile.close()

Tools.createObjFile(testTweetsList,'Test_tweets.obj')
print "Reading of test tweets finish!!!!"
