import tweepy
import tweepy.api


def twitters(key, sec, tok, toks, number_of_tweets):
    try:
        auth = tweepy.OAuthHandler(key, sec)
        auth.set_access_token(tok, toks)
        api = tweepy.API(auth)
        tweets = api.user_timeline()[:number_of_tweets]
        tweets_list = []
        for tweet in tweets:
            tweets_list.append('@' + tweet.author.name + ' ' + tweet.text)
        return tweets_list
    except Exception as e:
        return e


def tweetit(user, tweet):
    try:
        auth = tweepy.OAuthHandler(user.consumer_key, user.consumer_secret)
        auth.set_access_token(user.access_token, user.access_token_secret)
        api = tweepy.API(auth)
        api.update_status(tweet)
        return "<span class='alert alert-info'>Successfully updated!</span>"
    except Exception as e:
        return "<span class='alert alert-error'>%s></span>" % (str(e))
