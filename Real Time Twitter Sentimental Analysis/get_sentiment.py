import instinct

#It is the main file which runs, when the users click the search button
def getSentiment(query):

	try:
		#Creating the TwitterClient Object
		api = instinct.TwitterClient()

		#Getting the 300 tweets from tweepy
		tweets=api.get_tweets(query,300)

		#Creatig the list of positive and negative tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

		#In case there is no tweet found on a query
		if len(tweets) is 0:
			return {"Result":"No tweet found on this name."}
		#Otherwise return the dictionary with the positive and negative tweet percentage
		return {"Negative tweets percentage": 100*len(ntweets)/len(tweets),"Positive tweets percentage":100*len(ptweets)/len(tweets)}
	except:
			{"ERROR":"API connection failed."}

''' 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text']) 
'''