import twitter
import pickle 

#Setting up Twitter API
api = twitter.Api(
 consumer_key='...',
 consumer_secret='...',
 access_token_key='...',
 access_token_secret='...'
 )

twitterTrainFile = open("100_topics_100_tweets.sentence-three-point.subtask-A.train.gold.txt", "r")
#twitterTrainFile = open("kati.txt", "r")
data = twitterTrainFile.readlines()
traintweets_list = []
NumberOfDocuments=0
for line in data:
    tweet = line.split()
    try:
        status = api.GetStatus(status_id = tweet[0])
        traintweets_list.append((tweet[0], status.text, tweet[1]))
        NumberOfDocuments+=1
        print NumberOfDocuments
    except:
        continue
    
twitterTrainFile.close()

#df = pd.DataFrame(traintweets_list)

object_pi=traintweets_list
file_pi = open('Train_tweets.obj', 'w') 
pickle.dump(object_pi, file_pi) 
file_pi.close()

print "Finished!!!!"
