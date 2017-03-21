from requests_oauthlib import OAuth1

# Put your credentials here // https://apps.twitter.com
consumer_key         = ''
consumer_key_secret  = ''
access_token         = ''
access_token_secret  = ''

# Twitter API calls
base_twitter_url = 'https://api.twitter.com/1.1/'

oauth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)