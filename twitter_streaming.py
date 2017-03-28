# -*- coding: utf-8 -*-

from twitter_keys import *

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import json, requests

# List with screen names or user IDs to follow
follow = ['JarleBrenna', '817668451']


#
# Get user id if screen name is used
#
def get_id(screen_name):

	url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=%s" % (screen_name)

	response = requests.get(url,auth=oauth)

	if response.status_code == 200:
		
		result = json.loads(response.content)

		for row in result:
		    user_id = row['id']
		
		return user_id
	
	return None



class StdOutListener(StreamListener):
   
    # 
    # Receives messages as they come in from Twitter
    #
    def on_data(self, data):
        
        # convert from JSON to a dictionary
        tweet = json.loads(data)
        
        # log the Tweet to a file
        fd = codecs.open("tweets.log","ab",encoding="utf-8")
        fd.write("%s\r\n" % tweet)
        fd.close()
        
        # print the tweet out
        print tweet
        
        return True

    #
    # Receives error messages from the Twitter API
    #
    def on_error(self, status):
        print "[!] ERROR: %s" % status


# Script start
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Get id if screen_name is used
for n,i in enumerate(follow):
	if not i.isdigit():
		follow[n] = str(get_id(i))

stream = Stream(auth, l)
stream.filter(follow)