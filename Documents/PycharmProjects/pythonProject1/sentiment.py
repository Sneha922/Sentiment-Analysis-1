
import matplotlib.pyplot as plt
import os
import uuid

import tweepy
import csv
import re
from textblob import TextBlob
import matplotlib

matplotlib.use('agg')


# class with main logic
class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    # This function first connects to the Tweepy API using API keys
    def DownloadData(self, keyword, tweets):

        # authenticating
        consumerKey = 'uzZYzPHC7mmbEIfetivVi7y8Z'
        consumerSecret = 'OVK8VLqr82LmqJcKtp3BD5WNDyqKfFMhMgk5rQKbMaoAdYt19o'
        accessToken = '1422561373628760065-oBKURjRmltybQccmM1TDi7aErJyOXz'
        accessTokenSecret = 'GI1hI2d9q8FYRlFLZjiaMr6zeBhTaXDY1AbolfjhRnsqo'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # input for term to be searched and how many tweets to search
        # searchTerm = input("Enter Keyword/Tag to search about: ")
        # NoOfTerms = int(input("Enter how many tweets to search: "))
        tweets = int(tweets)

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=keyword, lang="en").items(tweets)

        # Open/create a file to append data to
        # csvFile = open('result.csv', 'a')

        # Use csv writer
        # csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        happy = 0
        fear = 0
        sad = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:

            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))

            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)

            # print(analysis.sentiment)  # print tweet's polarity
            # adding up polarities to find the average later
            polarity += analysis.sentiment.polarity

            # adding reaction of how people are reacting to find average later
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
                happy += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                fear += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.3):
                sad += 1

        # Write to csv and close csv file
        # csvWriter.writerow(self.tweetText)
        # csvFile.close()

        # finding average of how people are reacting
        happy = self.percentage(happy, tweets)
        fear = self.percentage(fear, tweets)
        sad = self.percentage(sad, tweets)
        neutral = self.percentage(neutral, tweets)

        # finding average reaction
        polarity = polarity / tweets

        # printing out data
        #  print("How people are reacting on " + keyword + " by analyzing " + str(tweets) + " tweets.")
        #  print()
        #  print("General Report: ")

        if (polarity == 0):
            htmlpolarity = "Neutral"

        # print("Neutral")
        elif (polarity > 0 and polarity <= 1):
            htmlpolarity = "Happy"
        elif (polarity > -0.1 and polarity <= 0):
            htmlpolarity = "Fear"
        elif (polarity > -1 and polarity <= -0.1):
            htmlpolarity = "Sad"

        imageid= self.plotPieChart(happy, fear, sad, neutral, keyword, tweets)

        print(polarity, htmlpolarity)
        return polarity, htmlpolarity, happy, fear, sad, neutral, keyword, tweets, imageid

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    # function which sets and plots the pie chart. The chart is saved in an img file every time the project is run.
    # The previous image is overwritten. This image is called in the html page.

    def plotPieChart(self, happy, fear, sad, neutral, keyword, tweets):
        fig = plt.figure()
        labels = ['Happy [' + str(happy) + '%]', 'Fear [' + str(fear) + '%]',
                  'Sad [' + str(sad) +
                  '%]', 'Neutral [' + str(neutral) + '%]']
        sizes = [happy, fear, sad,
                 neutral]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen',
                  'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        strFile = "./static/"+str(uuid.uuid1())+".png"
        if os.path.isfile(strFile):
            os.remove(strFile)  # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
        return strFile

