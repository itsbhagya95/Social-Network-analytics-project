import datetime
from tweepy_class import ExtractTweet
import csv


def main():
    """
    main function to call twitter API
    """
    input_data = {
        "text_query": "F1",  # change it if you want to search based on keyword
        "start_date": datetime.datetime(2022, 4, 29),
        "until_date": datetime.datetime(2022, 5, 5),
        "max_tweets":500,
        "user_id": "@F1" # change it if you want to search based on user_id
    }

    all_tweets = extract_data_based_on_user_input(input_data)
    print(all_tweets)
    all_tweets.to_csv("F1.csv")


def extract_data_based_on_user_input(input_data):
    """
    show user_input and display data
    :param input_data:
    :return: all_tweets
    """
    obj = ExtractTweet(input_data)
    api = obj.auth_twitter_account()
    all_tweets = None
    print("************ HELLO, HOW DO YOU WANT TO SEARCH? ************")
    print()
    print("1. By Keyword")
    print()
    print("2. By User")
    print()
    user_input = input("choose any one: ")
    print()
    if user_input == "1":
        print(f"     Selected keyword -> {input_data['text_query']}      ")
        print()
        all_tweets = obj.search_tweet_on_keyword(api)
    elif user_input == "2":
        print(f"     Selected User_id -> {input_data['user_id']}         ")
        print()
        all_tweets = obj.search_tweet_based_on_user(api)
    else:
        print("!!! Wrong input...Please try again")

    return all_tweets


if __name__ == "__main__":
    main()
