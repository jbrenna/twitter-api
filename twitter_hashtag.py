# -*- coding: utf-8 -*-

from twitter_keys import *
import requests, json, time, urllib, csv, codecs


# Twitter query operators: https://dev.twitter.com/rest/public/search
keyword = "#politikk"

# Logfile
logfile = 'hashtag.csv'



#
# Send keyword to Twitter API
#
def send_keyword_request(keyword, max_id=None):

	keyword = { 'q' : keyword }
	url = "https://api.twitter.com/1.1/search/tweets.json?%s" % urllib.urlencode(keyword)
 
	if max_id is not None:
		url += "&max_id=%d" % max_id 

	# send request to Twitter
	response = requests.get(url,auth=oauth)
	
	if response.status_code == 200:
		
		tweets = json.loads(response.content)
		
		return tweets
	
	return None


#
# Takes a keyword
#
def keyword_search(keyword):
	keyword_tweet_list  = []
	max_id          = 0
	
	# grab the first 200 Tweets
	tweet_list      = send_keyword_request(keyword)
	
	# grab the oldest Tweet
	oldest_tweet = tweet_list['statuses'][-1]
	
	# continue retrieving Tweets
	while max_id != oldest_tweet['id']:
	
		keyword_tweet_list.extend(tweet_list['statuses'])
 
		# set max_id to latest max_id we retrieved
		max_id = oldest_tweet['id']         
 
		print "[*] Retrieved: %d Tweets (max_id: %d)" % (len(keyword_tweet_list),max_id)
	
		# sleep to handle rate limiting
		time.sleep(3)
		
		# send next request with max_id set
		tweet_list = send_keyword_request(keyword,max_id-1)
	
		# grab the oldest Tweet
		if len(tweet_list['statuses']):
			oldest_tweet = tweet_list['statuses'][-1]
	
	# return the full Tweet list
	return keyword_tweet_list


#
# Write tweets to file
#    
def log_results(tweets, logfile):
    import codecs
    
    fd = codecs.open(logfile,"wb",encoding="utf-8")
    fd.write("id,created,username,text,retweets\r\n")
    
    for tweet in tweets:
        
        output = "%f,%s,%s,%s,%s" % (tweet['id'], tweet['created_at'], tweet['user']['screen_name'], tweet['text'], tweet['retweet_count'])
        
        print output
        
        fd.write(output+"\r\n")
    
    fd.close()
 
    return    


# Script start
keyword_tweet_list = send_keyword_request(keyword)

log_results(keyword_tweet_list['statuses'], logfile)