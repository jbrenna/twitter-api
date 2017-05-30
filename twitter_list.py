#!/usr/bin/python
# -*- coding: utf-8 -*-

from twitter_keys import *
import requests, json

slug = "politikere"
screen_name = "JarleBrenna"

#
# Get twitter profiles from list
#
count = 0

api_url  = "%s/lists/members.json?" % base_twitter_url
api_url += "slug=%s&" % slug
api_url += "owner_screen_name=%s&count=5000" % screen_name

response = requests.get(api_url,auth=oauth)

if response.status_code == 200:
  result = json.loads(response.content)

  for row in result['users']:
    count = count +1

    print "#%d - %d: %s" % (count, row["id"], row["screen_name"])

else:
  print "Something is wrong. List could be private."
