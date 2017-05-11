# -*- coding: utf-8 -*-

import re

from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.tag.perceptron import PerceptronTagger as AveragedPerceptronTagger

from earthy.nltk_wrappers.downloader import NLTKDownloader

class NLTKWordTokenizer(TreebankWordTokenizer):
    def __init__(self):
        # Initialize the standard TreebankWordTokenizer.
        super(self.__class__, self).__init__()
        # Adding to TreebankWordTokenizer, the splits on
        # - chervon quotes u'\xab' and u'\xbb' .
        # - unicode quotes u'\u2018', u'\u2019', u'\u201c' and u'\u201d'
        improved_open_quote_regex = re.compile(u'([«“‘])', re.U)
        improved_close_quote_regex = re.compile(u'([»”’])', re.U)
        improved_punct_regex = re.compile(r'([^\.])(\.)([\]\)}>"\'' u'»”’ ' r']*)\s*$', re.U)
        self.STARTING_QUOTES.insert(0, (improved_open_quote_regex, r' \1 '))
        self.ENDING_QUOTES.insert(0, (improved_close_quote_regex, r' \1 '))
        self.PUNCTUATION.insert(0, (improved_punct_regex, r'\1 \2 \3 '))
