from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark import SparkContext
import pandas as pd

import itertools

if __name__ == '__main__':
    # create the Spark Session
    spark = SparkSession.builder.getOrCreate()

    sc = SparkContext.getOrCreate()
    lines = sc.textFile('data/soc-LiveJournal1Adj.txt')
    lines = lines.map(lambda line:line.split())
    friends = lines.filter(lambda x:len(x)==2).map(lambda x:(x[0],x[1].split(','))) # map friends to user

    # create a list of direct friends and mutual friends
    directFriends = friends.flatMap(lambda data:[((data[0],friend), -9999) for friend in data[1]]) # -9999 is used to differentiate direct friends from mutual friends
    mutualFriends = friends.flatMap(lambda data: [(pair, 1) for pair in itertools.permutations(data[1], 2)]) # map pairs of friends
    fullList = directFriends.union(mutualFriends) # combine direct and mutual friends

    # count the number of mutual friends
    fullList = fullList.reduceByKey(lambda x,y: x+y)
    mutualCount = fullList.filter(lambda x:x[1]>0) # filter out direct friends
    mutualCount = mutualCount.map(lambda x:(x[0][0],(x[0][1], x[1]))) # map to user and number of mutual friends
    mutualCount = mutualCount.groupByKey().mapValues(list) # group by user

    # sort the list of recommendations
    # If there are recommended users with the same number of mutual friends, then output those user IDs in numerically ascending order.
    # First sort by number of mutual friends, then by user ID
    mutualCount = mutualCount.mapValues(lambda recommendations: sorted(recommendations, key=lambda x: (-x[1], x[0]))[:10])

    active = mutualCount.collect()  # collect the list of recommendations

    # output the result
    for i in range(len(active)):
        active[i] = str(active[i][0]) + "\t" + ",".join(str(item) for item in active[i][1]) # format the output
    noFriends = lines.filter(lambda x:len(x)==1) # filter users with no friends
    noFriends = noFriends.flatMap(lambda x:x).collect()  # collect the list of users with no friends
    full = active + noFriends
    sc.parallelize(full).repartition(1).saveAsTextFile('output')
    sc.stop()
