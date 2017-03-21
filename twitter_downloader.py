# -*- coding: utf-8 -*-

from twitter_keys import *

import requests
import json
import time


# Set profile and logfile
user = ''
logfile = 'tweets.csv'


#
# Download Tweets from profile
#
def download_tweets(screen_name,number_of_tweets,max_id=None):
    
    api_url  = "%s/statuses/user_timeline.json?" % base_twitter_url
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=%d" % number_of_tweets
    
    if max_id is not None:
        api_url += "&max_id=%d" % max_id

    # send request to Twitter
    response = requests.get(api_url,auth=oauth)
    
    if response.status_code == 200:
        
        tweets = json.loads(response.content)
        
        return tweets
    

    return None


#
# Download all Tweets
#
def download_all_tweets(username):
    full_tweet_list = []
    max_id          = 0
    
    # grab the first 200 Tweets
    tweet_list   = download_tweets(username,200)
    
    # grab the oldest Tweet
    oldest_tweet = tweet_list[-1]
    
    # continue retrieving Tweets
    while max_id != oldest_tweet['id']:
    
        full_tweet_list.extend(tweet_list)

        # set max_id to latest max_id we retrieved
        max_id = oldest_tweet['id']         

        print "[*] Retrieved: %d Tweets (max_id: %d)" % (len(full_tweet_list),max_id)
    
        # sleep to handle rate limiting
        time.sleep(3)
        
        # send next request with max_id set
        tweet_list = download_tweets(username,200,max_id-1)
    
        # grab the oldest Tweet
        if len(tweet_list):
            oldest_tweet = tweet_list[-1]
        
    # add the last few Tweets
    full_tweet_list.extend(tweet_list)
        
    # return the full Tweet list
    return full_tweet_list 


#
# Write tweets to file
#    
def log_results(tweets,logfile):
    import codecs
    
    fd = codecs.open(logfile,"wb",encoding="utf-8")
    fd.write("id,created,text,retweets\r\n")
    
    for tweet in tweets:
        
        output = "%f,%s,%s,%s" % (tweet['id'], tweet['created_at'], tweet['text'], tweet['retweet_count'])
        
        print output
        
        fd.write(output+"\r\n")
    
    fd.close()
 
    return    


# script start
full_tweet_list = download_all_tweets(user)

log_results(full_tweet_list,logfile)