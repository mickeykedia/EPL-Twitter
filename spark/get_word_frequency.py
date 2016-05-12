import json
from datetime import datetime
from pyspark import SparkContext, SparkConf


def split_words_into_list(phrase):
    arr = phrase.split(" ")
    new_arr = []
    for a in arr:
        if a:
            new_arr.append(a)
    return new_arr

def load_string_to_json(x):
    d = {'lang':'garbage'}
    try:
        d = json.loads(x)
    except ValueError:
        pass
    finally:
        return d

def change_timestamp_to_time(tup):
    """
    Convert timestamp to dayhourminute
    """
    dt = datetime.utcfromtimestamp(int(tup[0])//1000)
    
    return (str(dt.day)+str(dt.hour)+str(dt.minute), tup[1])

def concatenateLists(x,y):
    x.extend(y)
    return x

def create_frequency_dict(list_tweets):
    d = {}
    for arr in lw.value:
        d[arr[0]] = 0
    for tweet in list_tweets:
        lt = str.lower(tweet.encode('utf-8'))
        for arr in lw.value:
            for a in arr:
                if a in lt:
                    d[arr[0]] += 1
                    break
    return d

words= """
title 
Rashford 
Kane
alderweireld 
Diego costa 
eden hazard
mourinho jose
stamford
everton
Mousa dembele
Willian
Pochettino Mauricio
Cahill
Fabregas
Lamela
Ref Referree 
champions
leicester
foxes
mourinho
penalty 
vardy
mahrez 
claudio ranieri
guus hiddink
Heung-Min Heung
eye gouging gouge
Vertonghen
Walker Kyle
"""

#conf = SparkConf().setAppName("wfc").setMaster(master)
#sc = SparkContext(conf=conf)

words = str.lower(words).split("\n")
words = words[1:len(words)-1]
list_words = map(split_words_into_list, words)
lw = sc.broadcast(list_words)
sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId",'AKIAI3CQ4KIGL6KYRABQ')
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", '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')

folderList = ['epl-twitter/raw-data2016/05/02/19/*', 'epl-twitter/raw-data2016/05/02/20/*']
tweets = sc.textFile(",".join(folderList)).map(lambda x:x.rstrip(",")).map(load_string_to_json) 

time_tweet = tweets.filter(lambda x: x['lang']=="en").map(lambda x: (x['timestamp_ms'], [x['text']]))
time_tweet.cache()
time_tweet = time_tweet.map(change_timestamp_to_time)

time_multiple_tweets = time_tweet.reduceByKey(concatenateLists)

time_freq = time_multiple_tweets.map(lambda x: (x[0], create_frequency_dict(x[1])))

data = time_freq.collectAsMap()
