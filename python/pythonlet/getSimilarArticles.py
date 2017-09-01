#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import urllib2
import json
import spacy
import pprint
import re
from optparse import OptionParser


# consts
# example: https://newsapi.org/v1/articles?source=techcrunch&apiKey={API_KEY}
API_KEY = '' # test only, [to be removed]
API_URL = 'https://newsapi.org/v1/articles?source={0}&apiKey={1}'
LATEST_NEWS_COUNT = 10
SCRIPTS_USAGE = """Usage:
1) install spacy libs and its model by:
    sudo pip install spacy
    python -m spacy download en
          
2) run the script:
{0} [-d|--dryrun] -k|--api-key api_key -t|--text text
\tdryrun:  use local topnews.json file to tes, for not connecting to newsapi.org case.
\tapi_key: the API key used to get top news from ex. 
\t         {1}
\ttext:    the input text to be checked against the top news, ended with Enter key.
""".format(sys.argv[0], API_URL.format('google-news', '{API_KEY}'))

DETECTOR_USAGE = """Usage:\nto detect the similarity of input text to given top API news.

    detector = SimilarArticlesDetector()
    detector.check_similarity()

"""


# classes
class SimilarArticlesDetector(object):
    def __init__(self, news_src_name='google-news', api_key=API_KEY):
        self.news_src_name = news_src_name.lower().replace(' ', '-')
        self.api_key = api_key
        self.data = ''
        self.dryrun = False
        self.news_set = set([])
        self.similarity_list = []

    def get_input(self):
        try:
            parser = OptionParser()
            parser.add_option('-d', '--dryrun', dest='dryrun', help='use local topnews.json file to test', action='store_true', default=False)
            parser.add_option('-k', '--api-key', dest='api_key', help='API key used to get top news from {0}'.format(API_URL))
            parser.add_option('-t', '--text', dest='text', help='text to be checked against the top news')
            options, _ = parser.parse_args()
            self.api_key = options.api_key
            if options.text:
                self.data = options.text.strip(string.whitespace)
            self.dryrun = options.dryrun
        except IndexError as e:
            print('[Error] Exception: {0}\n\n{1}'.format(e.message, SCRIPTS_USAGE))
            raise(e)
        if self.data == '':
            print('[INFO] No input is given.\n\n{0}'.format(SCRIPTS_USAGE))
            raise(Exception('Empty text.'))

    def get_topnews_from_api(self, news_src_name, api_key):
        print('[INFO] to get news from {0} ...\n'.format(news_src_name))
        url = API_URL.format(news_src_name, api_key)
        try:
            res = urllib2.urlopen(url).read()
            res_json = json.loads(res, 'utf-8')
            self.news_set = set(a['title'] for a in res_json['articles'] if 'title' in a)
        except Exception as e:
            print('[Error] No articles can be got from {0} with api_key {1}.\n{2}\n'.format(news_src_name, api_key, e.message))
            raise(e)
        
    # function only for local test
    def get_topnews_from_localfile(self):
        print('[INFO] to get news from local file ...\n')
        try:
            with open('topnews.json', 'r') as f:
                res = f.read()
            res = re.sub(r'(:\s*?".*?)\\"(.*?)\\"(.*?,)', r'\1\2\3', res)
            res = re.sub(r'\s*-\s*\n', '', res)
            res_json = json.loads(res, 'utf-8')
            self.news_set = set(a['title'] for a in res_json['articles'] if 'title' in a)
        except Exception as e:
            print('[Error] No articles can be got from the local file.')
            raise(e)
        
    def calculate_similarity(self, checker_data, checkee_set):
        try:
            nlp = spacy.load('en')
            data_nlped = nlp(unicode(checker_data))
            self.similarity_list = [(data_nlped.similarity(nlp(unicode(title))), title) for title in checkee_set]
            self.similarity_list.sort(reverse=True)
        except Exception as e:
            print('[Error] calculate similarity failed.\n{0}\n'.format(e.message))
            raise(e)

    def check_similarity(self):
        try:
            self.get_input()
            if self.dryrun:
                self.get_topnews_from_localfile()
            else:
                self.get_topnews_from_api(self.news_src_name, self.api_key)
            self.calculate_similarity(self.data, self.news_set)
            print('[INFO] similarity result:')
            pprint.pprint(self.similarity_list)
        except Exception as e:
            print('[Error] check similarity failed.\n{0}\n'.format(e.message))
            return



if __name__ == '__main__':
    try:
        detector = SimilarArticlesDetector()
        detector.check_similarity()
    except Exception as e:
        print('[Error] run SimilarArticlesDetector failed. Exist. {0}\n\n{1}'.format(e.message, DETECTOR_USAGE))

