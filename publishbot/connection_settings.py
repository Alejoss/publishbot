import tweepy


def twitter_connect():
    # Twitter API credentials
    consumer_key = "your_consumer_key"
    consumer_secret = "your_consumer_secret"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    # Create the API object
    try:
        # Authenticate with Twitter API using Tweepy library
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except tweepy.TweepError as e:
        print(f"Error connecting to Twitter API: {e}")
        return None

    return api


