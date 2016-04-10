from tweepy import OAuthHandler

access_token_key = ["<Enter Access Token Keys here>"]
access_token_secret = ["<Enter Access Token Secrets here>"]

consumer_key = ["<Enter Consumer Keys here>"]
consumer_secret = ["<Enter Consumer Secrets here>"]


length = len(access_token_key)


def get_auth_object(index):
    i = index % length
    auth = OAuthHandler(consumer_key[i], consumer_secret[i])
    auth.set_access_token(access_token_key[i], access_token_secret[i])
    return auth