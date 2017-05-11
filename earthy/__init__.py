# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import pickle
from itertools import chain

from earthy.nltk_wrappers import *

def download(name, download_dir=None, xml_url=None, quiet=False):
    """
    The data download function.
    (Currently, it's wrapping NLTK's downloader.)
    """
    # Create the Downloader object.
    global _nltk_downloader
    try:
        _nltk_downloader
    except NameError:
        _nltk_downloader = NLTKDownloader(download_dir, xml_url)
    _nltk_downloader.download(name, quiet=quiet)


def sent_tokenize(text, lang='english'):
    """
    Punkt sentence tokenizer from NLTK.
    """
    global _nltk_sent_tokenizer
    try:
        _nltk_sent_tokenizer
    except NameError:
        # If the sentence tokenizer wasn't previously initialized.
        available_languages = ['czech', 'danish', 'dutch', 'english',
                               'estonian', 'finnish', 'french', 'german',
                               'greek', 'italian', 'norwegian', 'polish',
                               'portuguese', 'slovene', 'spanish', 'swedish',
                               'turkish']
        assert lang in available_languages, "Punkt Tokenizer for {} not available".format(lang)
        # Checks that the punkt tokenizer model was previously downloaded.
        download('punkt', quiet=True)
        path_to_punkt = _nltk_downloader._download_dir + '/tokenizers/punkt/{}.pickle'.format(lang)
        with open(path_to_punkt, 'rb') as fin:
            _nltk_sent_tokenizer = pickle.load(fin)
    # Actual tokenization using the Punkt Model.
    return _nltk_sent_tokenizer.tokenize(text)


def word_tokenize(text, keep_lines=False):
    """
    Improved treebank tokenizer from NLTK.
    """
    global _nltk_word_tokenizer
    try:
        _nltk_word_tokenizer
    except NameError:
        _nltk_word_tokenizer = NLTKWordTokenizer()
    if keep_lines:
        return _nltk_word_tokenizer.tokenize(text)
    else:
        return list(chain(*map(_nltk_word_tokenizer.tokenize, sent_tokenize(text))))


def pos_tag(tokenized_text):
    """
    Averaged perceptron tagger from NLTK (originally from @honnibal)
    """
    global _nltk_pos_tagger
    try:
        _nltk_pos_tagger
    except NameError:
        _nltk_pos_tagger = AveragedPerceptronTagger()
        # Checks that the punkt tokenizer model was previously downloaded.
        download('averaged_perceptron_tagger', quiet=True)
    return _nltk_pos_tagger.tag(tokenized_text)

pos_tag(word_tokenize('earthy'))
