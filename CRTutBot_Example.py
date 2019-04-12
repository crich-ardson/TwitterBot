from __future__ import print_function
import tweepy
from CRTutBot_Access_Example import consumer_key, consumer_secret, access_token, access_token_secret
from io import *

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
auth.secure = True
api = tweepy.API(auth, wait_on_rate_limit=True)

#Find list of accounts that follow the bot. Follow any unfollowed account
def follow():
    for follower in tweepy.Cursor(api.followers).items():
        try:
            follower.follow()

        except tweepy.TweepError as e:
            print (e.reason)
            continue
        except StopIteration:
            break
    return None

#function to process tweets
def process_tweets(tweet, id_list):
    if tweet.id in id_list:
        print("already found this one")
    else:
        print("Processing new tweet by @" + tweet.user.screen_name)
        tweet.favorite()
        if (tweet.retweet_count <= 100):
            tweet.retweet()

#Gather tweets made by the bot and store ids while also writing them to a .txt file
ids = []
record = open("storage.txt","a+")

my_tweets = api.user_timeline(api,count=200)

for tweet in my_tweets:
    ids.append(tweet.id)
    record.write(unicode(str(tweet.id),"utf-8")+ "\n")
    
record.close()

#supporting variables for gathering tweets
id_track = ids[-1] - 1
container = []

#Gather tweets according to the searched hashtag since the most recent retweet by the bot. Favorite and Retweet the found tweet
container = tweepy.Cursor(api.search, q='#blackarts', rpp=20, since_id=id_track).items(600)

for tweet in container:
    try:
        process_tweets(tweet, ids)

    except tweepy.TweepError as e:
        print(e.reason)
        continue
    except StopIteration:
        break



follow()

