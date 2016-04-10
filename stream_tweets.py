import argparse
from tweepy import Stream
from tweepy.streaming import StreamListener
from credentials import get_auth_object


class TweetListener(StreamListener):

    def __init__(self, file_name):
        self._file_name = file_name

    def on_data(self, data):
        try:
            with open(self._file_name, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', required=True, help='Enter the output file name')
    parser.add_argument('-index', help='Enter the Index of the auth credentials to use', type=int)
    parser.add_argument('-terms', nargs='+', help='Enter the search terms')

    opts = parser.parse_args()
    file_name = opts.f
    terms = ','.join(opts.terms)
    index = opts.index
    
    auth = get_auth_object(index)
    tweet_listener = TweetListener(file_name)
    twitter_streamer = Stream(auth, tweet_listener)
    twitter_streamer.filter(track=[terms])