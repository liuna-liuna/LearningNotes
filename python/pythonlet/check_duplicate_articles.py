#!/usr/bin/env python
# -*- coding: utf-8 -*-


articles = list()
# [TODO] init articles

# brutal force
def is_duplicate(input_article):
    if not input_article or not articles: 
      return None
    duplicated_article_id = []
    input_splitted = input_article.split()
    seen = set()
    for input_i, input_a in enumerate(input_splitted):
      for i, a in enumerate(articles):
        if i in seen:
          continue
        index = a.find(input_a)
        if index == -1:
          continue
        input_i_new, counts = input_i+1, 0
        while input_i_new < len(input_splitted) \
          and index+1 < len(a) \
          and input_splitted[input_i_new] == a[index+1]:
            input_i_new += 1
            index += 1
            counts += 1
        if counts >= 100:
          duplicated_article_id.append(i)
          seen.add(i)
          break
    return duplicated_article_id


# built-in lib
"""use difflib.SequenceMatcher

# ref:  https://stackoverflow.com/questions/17388213/find-the-similarity-percent-between-two-strings
# ref:  http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/


"""
def is_duplicate(input_article):
    if not input_article or not articles: 
      return None
    import difflib
    leni = len(input_article)
    duplicated_article_id = []
    for i, a in enumerate(articles):
        sm = difflib.SequenceMatcher(None, input_article, a)
        if sm.find_longest_match(0, leni, 0, len(a)).size >= 100:
            duplicated_article_id.append(i)
    return duplicated_article_id





