import argparse
import json
import tweepy
from credentials import get_auth_object


def search_tweets(auth_obj, data_file_name):
    api = tweepy.API(auth_obj)
    max_id = None
    search_data = {'tweets': []}
    for i in range(0, 5):
        search_results = api.search(terms, count=100, max_id=max_id)
        for text in search_results:
            search_data['tweets'].append(text.text)
        if search_results.next_results:
            max_id_fragment = search_results.next_results.split('&')[0]
        else:
            break
        max_id = max_id_fragment.split('=')[-1]
    with open(data_file_name, 'w') as data_file:
        data_file.write(json.dumps(search_data))


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
    search_tweets(auth, file_name)