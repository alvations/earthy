# -*- coding: utf-8 -*-

from earthy.wordlist import punctuations, stopwords
from earthy.nltk_wrappers import word_tokenize


def remove_stopwords(text, lang='en', custom_stoplist=None, remove_punct=True):
    _stopwords = set(custom_stoplist)if custom_stoplist else set(stopwords[lang])
    if remove_punct:
        _stopwords = _stopwords | punctuations
    for word in word_tokenize(text):
        if word.lower() not in _stopwords:
            yield word
