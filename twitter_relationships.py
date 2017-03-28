# -*- coding: utf-8 -*-

from twitter_keys import *
import json, requests, time


# Screen name of profile
username = 'JarleBrenna'
 
 
#
# Main Twitter API function for sending requests
#
def send_request(screen_name, relationship_type, next_cursor=None):
 
    api_url = 'https://api.twitter.com/1.1/%s/ids.json' % relationship_type
 
    params = {
        'screen_name':  screen_name,
        'count':        5000,
    }
 
    if next_cursor is not None:
        params['cursor'] = next_cursor
 
    response = requests.get(api_url, params=params, auth=oauth)
 
    time.sleep(3)
 
    if response.status_code == 200:
 
        result = json.loads(response.content)
 
        return result
 
    return None


# Function that contains the logic for paging through results
#
def get_all_friends_followers(username, relationship_type):
 
    account_list = []
    next_cursor  = None
    accounts     = {}
 
    while next_cursor not in (-1,0):
 
        accounts    = send_request(username, relationship_type, next_cursor)
 
        # break out of the loop if we don't receive any accounts
        # or the call fails
        if accounts is None:
 
            break
 
        account_list.extend(accounts['ids'])
 
        print '[*] Downloaded %d of type %s' % (len(account_list), relationship_type)
 
        next_cursor = accounts.get('next_cursor', None)
 
    return account_list


#
# Write to file
#    
def log_results(users, logfile):
    import codecs
    
    fd = codecs.open(logfile,"wb",encoding="utf-8")
    fd.write("id,username\r\n")
    
    for user in users:

        # get username
        url = "https://api.twitter.com/1.1/users/lookup.json?%s=%s" % ('user_id', user)
        response = requests.get(url,auth=oauth)

        result = json.loads(response.content)

        if response.status_code == 200:
            for row in result:
                username = row['screen_name']
        
                output = "%f,%s" % (user, username)
        
                print output
        
                fd.write(output+"\r\n")
        else:
            print result['errors'][0]['message']

        # sleep to handle rate limiting
        time.sleep(1)
    
    fd.close()
 
    return  


# script start
friends   = get_all_friends_followers(username, 'friends')
followers = get_all_friends_followers(username, 'followers')
 
print '[**] Retrieved %d friends' % len(friends)
print '[**] Retrieved %d followers' % len(followers)
 
snapshot_timestamp = time.time()
 
# store the friends
logfile = '%s-%f-friends.txt' % (username, snapshot_timestamp)
log_results(friends, logfile)
 
print '[!] Stored friends in %s' % logfile 
 
# store the followers
logfile = '%s-%f-followers.txt' % (username, snapshot_timestamp)
log_results(followers, logfile)

print '[!] Stored followers in %s' % logfile