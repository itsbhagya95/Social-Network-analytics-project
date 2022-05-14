"""
class file to extract data from twitter for a specific time
"""

import tweepy
import keys
from tweepy import OAuthHandler
import pandas as pd
import time


class ExtractTweet:
    """
    Main class to extract tweet using tweepy
    """

    def __init__(self, input_data):
        """
        initialization of required variabled
        :param input_data:
        """
        self.consumer_key = keys.API_KEY
        self.consumer_secret = keys.API_KEY_SECRET
        self.access_token = keys.ACCESS_TOKEN
        self.access_token_secret = keys.ACCESS_TOKEN_SECRET
        self.text_query = input_data["text_query"]
        self.start_date = input_data["start_date"]
        self.until_date = input_data["until_date"]
        self.max_tweets = input_data["max_tweets"]
        self.df_tweets = pd.DataFrame()
        self.list_of_tweets = []
        self.user_id = input_data["user_id"]

    def auth_twitter_account(self):
        """
        authenticate Tweepy API with keys
        :return: api object
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(
            auth,
            retry_count=2,
            retry_delay=10,
            wait_on_rate_limit=True,
            retry_errors=set([401, 404, 500, 503])
        )
        return api

    def search_tweet_on_keyword(self, api):
        """
        search tweet based on keyword
        :param api: api object of tweepy
        :return: dataframe of tweets
        """
        try:
            tweets = tweepy.Cursor(
                api.search_tweets,
                q=self.text_query,
                until=self.until_date
            ).items(self.max_tweets)
            df_tweets = self.create_df_tweets(tweets, search_type="search")
            return df_tweets
        except BaseException as e:
            print(str(e))
            time.sleep(2)

    def search_tweet_based_on_user(self, api):
        """
        search tweet based on user_id
        :param api:
        :return: dataframe of tweets
        """
        try:
            tweets = api.user_timeline(screen_name=self.user_id,
                                       count=self.max_tweets,
                                       )
            df_tweets = self.create_df_tweets(tweets, search_type="user_id")
            return df_tweets
        except BaseException as e:
            print(str(e))
            time.sleep(2)

    def create_df_tweets(self, tweets, search_type):
        """
        create a dataframe from list of tweets
        :param tweets: list of tweets
        :param search_type: type of search (allowed values -> search, user_id)
        :return:
        """
        tweet_data = {}
        for tweet in tweets:
           if self.start_date.strftime('%Y-%m-%d') <= tweet.created_at.strftime('%Y-%m-%d') <= self.until_date.strftime('%Y-%m-%d'):
                tweet_data = {
                    'Created at': tweet._json['created_at'] if search_type == "search" else tweet.created_at,
                    'Text': tweet._json['text'] if search_type == "user_id" else tweet.text
                }
                self.list_of_tweets.append(tweet_data)
        df_tweets = self.df_tweets.append(self.list_of_tweets, ignore_index=True, sort=False)
        return df_tweets
