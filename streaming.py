import pymongo
import time
import datetime
import sys
try:
    import json
except ImportError:
    import simplejson as json


from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from prettytable import PrettyTable

def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):

    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]

    coll = db[mongo_db_coll]

    return coll.insert(data)


def load_from_mongo(mongo_db, mongo_db_coll, return_cursor=False,
                    criteria=None, projection=None, **mongo_conn_kw):

    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]

    if criteria is None:
        criteria = {}

    if projection is None:
        cursor = coll.find(criteria)
    else:
        cursor = coll.find(criteria, projection)

    if return_cursor:
        return cursor
    else:
        return [item for item in cursor ]


# Please input your own variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = 
ACCESS_SECRET = 
CONSUMER_KEY = 
CONSUMER_SECRET = 

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


twitter_stream = TwitterStream(auth=oauth)


q1 = ':)'
stream = twitter_stream.statuses.filter(track=q1, language="en")

tweet_count = 40000
for tweet in stream:
    tweet_count -= 1
    save_to_mongo(tweet, 'test-data8', 'positive_data3')
    if tweet_count <= 0:
        break

q2 = ':('
stream = twitter_stream.statuses.filter(track=q2, language="en")

tweet_count = 40000
for tweet in stream:
    tweet_count -= 1
    save_to_mongo(tweet, 'test-data8', 'negtive_data3')
    if tweet_count <= 0:
        break


