#!/usr/bin/env python
#sys.path.append(r"")
import get_twitter_data

## PLACE YOUR CREDENTIALS in config.json file or run this file with appropriate arguments from command line
keyword = 'iphone'
time = 'today'
twitterData = get_twitter_data.TwitterData()
tweets = twitterData.getTwitterData(keyword, time)
print tweets
