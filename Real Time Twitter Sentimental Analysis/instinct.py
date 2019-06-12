import re
import tweepy
import pickle
from tweepy import OAuthHandler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import sys
import pandas as pd
import numpy as np

 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'ibj4LJDm3g9hyLjl4Y5n5EJSX'
        consumer_secret = 'GxA9sStZWxuQykfCwYzjS0rtxLyMUPrcBfAXIHLM1BEjvr1fLE'
        access_token = '2713653055-prELIp7WxkCCm3zrttH1Wz9kCX0SmQ3rTM3xA3U'
        access_token_secret = 'lu5sxZHGxIGh5HK8LkSd0nr9zDgIEXToqMvcmFik7ud29'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")


        pos = []
        for line in open ('positive_tweets.json', 'r'):
            pos.append(json.loads(line))

        neg = []
        for line in open ('negative_tweets.json', 'r'):
            neg.append(json.loads(line))

        colname = ["text"]

        #Creating a 2-dimention list of positive tweets
        df0 = []
        for dic in pos:
            ll = []
            for c in colname:
                ll.append(dic[c])
            df0.append(ll)

        #Creating a 2-dimention list of negative tweets
        df1 = []
        for dic in neg:
            ll = []
            for c in colname:
                ll.append(dic[c])
            df1.append(ll)

        #Converting the positive sentiment data into data frame of pandas
        df0 = pd.DataFrame(df0, columns = colname)
        #Adding the column to set the semtiment of positive sentiments as 1
        df0["pn"] = 1
        #Converting the negative sentiment data into data frame of pandas
        df1 = pd.DataFrame(df1, columns = colname)
        #Adding the column to set the semtiment of negative sentiments as 0
        df1["pn"] = 0
        
        #Concatanating the positive and negative sentiment dataframe to a single data frame
        df = pd.concat([df0, df1], axis = 0, ignore_index = True)

        self.vectorizer = TfidfVectorizer(min_df = 3, use_idf = True)  
        train_x = self.vectorizer.fit_transform(df.text)


############################### MACHINE LEARNING IMPLEMENTATION ##########################################################


    def get_tweet_sentiment(self,tweet):

        #Removing the stop words i.e the useless words like @, special characters or links
        tweet = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|([A-Za-z]+:\/\/\S+)", " ", tweet).split())
        
        #Acessing the trained model
        file_name="finalised_model.sav"
        loaded_model = pickle.load(open(file_name,'rb'))

        #Predicting the sentiment of the tweet
        prediction = loaded_model.predict(self.vectorizer.transform([tweet]))
        if(str(prediction)=="[1]"):
            return "positive"
        else:
            return "negative"
    



##########################################################################################################################

    #Function to get the tweets
    def get_tweets(self,query,count):
      
        #Creating a list of dictionary of tweets 
        tweets = []
        #Getting teh tweets from tweepy on the query
        fetched_tweets = self.api.search(q=query,lang='en',count=count)

        for tweet in fetched_tweets:
            #Creating a dictionary to hold the tweet text and its sentiment for each tweet
            parsed_tweet = {}

            parsed_tweet['text']=tweet.text

            #Getting the sentiment of the tweet through our classifier model
            parsed_tweet['sentiment']=self.get_tweet_sentiment(tweet.text)

            #If the retweet count is greater than 0 and the tweet is already there in tweets list the drop this tweet 
            #otherwise add the tweet to tweets list
            if(tweet.retweet_count>0):
                if(parsed_tweet not in tweets):
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        #returning the list of tweets
        return tweets

