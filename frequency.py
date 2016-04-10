import argparse
import json
import re
import csv
from operator import itemgetter


def remove_stopwords(tweet, stopword_data):
    tweet_words = tweet.split()
    stopwords = stopword_data['stop_words']
    stoppatterns = stopword_data['stop_patterns']
    tweet_without_stopwords = []
    for word in tweet_words:
        cleaned_word = word.strip().strip('.').strip(',').strip('?').strip(':').strip(';')
        if cleaned_word.lower() not in stopwords and cleaned_word != '':
            for pattern in stoppatterns:
                if cleaned_word.find(pattern) == -1:
                    tweet_without_stopwords.append(cleaned_word)
    return tweet_without_stopwords


def clean_term(term):
    cleaned_term = re.sub('[^a-zA-Z0-9]', '', term)
    return cleaned_term.strip()


def compute_term_frequency(tweet_list):
    term_counts = {}
    term_frequencies = {}
    for tweet in tweet_list:
        for term in tweet:
            cleaned_term = clean_term(term)
            if cleaned_term != '':
                if term_counts.get(term):
                    term_counts[term] += 1
                else:
                    term_counts[term] = 1

    total_count_of_terms = sum(count for term, count in term_counts.items())

    for term, count in term_counts.items():
        term_frequency = count / total_count_of_terms
        term_frequencies[term] = term_frequency

    return term_frequencies


def extract_stopwords(stopword_file_name):
    with open(stopword_file_name) as stopword_file:
        stopword_data = json.loads(stopword_file.read())
    return stopword_data


def extract_tweets_from_data(tweet_data):
    tweets = []
    for tweet in tweet_data:
        tweets.append(tweet['text'])

    return tweets


def extract_search_tweets(tweet_file_name):
    with open(tweet_file_name) as tweet_file:
        tweets = json.loads(tweet_file.read())
    return tweets['tweets']


def extract_streaming_tweets(tweet_file_name):
    tweet_data = []
    with open(tweet_file_name) as tweet_file:
        for i in tweet_file:
            tweet = json.loads(i.strip())
            tweet_data.append(tweet)

    return tweet_data


def write_results_to_file(result_data, output_file_name):
    results = [{'Term': i[0], 'Frequency': i[1]} for i in result_data]
    with open(output_file_name, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=['Term', 'Frequency'])
        writer.writeheader()
        for result in results:
            writer.writerow(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tweet_file', required=True, help='Enter the name of the file with the tweets')
    parser.add_argument('-stopword_file', required=True, help='Enter the name of the stopwords file')
    parser.add_argument('-output_file', required=True, help='Enter the name of the output file')
    parser.add_argument('-input_type', required=True, help='\'st\' if the input file is a streaming or \'se\' if the input file is a search data file')
    opts = parser.parse_args()
    tweet_file_name = opts.tweet_file
    stopword_file_name = opts.stopword_file
    output_file_name = opts.output_file
    input_type = opts.input_type
    
    stopword_data = extract_stopwords(stopword_file_name)

    if input_type == 'se':
        tweets = extract_search_tweets(tweet_file_name)
    elif input_type == 'st':
        tweet_data = extract_streaming_tweets(tweet_file_name)
        tweets = extract_tweets_from_data(tweet_data)

    tweets_without_stopwords = [remove_stopwords(tweet, stopword_data) for tweet in tweets]
    
    term_frequencies = compute_term_frequency(tweets_without_stopwords)
    sorted_term_frequencies = sorted(term_frequencies.items(), key=itemgetter(1, 0), reverse=True)
    row = '{0}\t{1:.10f}'
    write_results_to_file(sorted_term_frequencies, output_file_name)

    for term_frequency in sorted_term_frequencies:

        print(row.format(term_frequency[0], term_frequency[1]))


if __name__ == '__main__':
    main()
