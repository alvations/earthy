# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import pickle

from earthy.downloader import Downloader
#from earthy.tokenize import TreebankTokenizer

def download(name, download_dir=None, xml_url=None, quiet=False):
    """
    The data download function.
    (Currently, it's wrapping NLTK's downloader.)
    """
    # Create the Downloader object.
    global _downloader
    try:
        _downloader
    except NameError:
        _downloader = Downloader(download_dir, xml_url)
    _downloader.download(name, quiet=quiet)


def sent_tokenize(text, lang='english'):
    """
    Punkt sentence tokenizer from NLTK.
    """
    global _sent_tokenizer
    try:
        _sent_tokenizer
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
        path_to_punkt = _downloader._download_dir + '/tokenizers/punkt/{}.pickle'.format(lang)
        with open(path_to_punkt, 'rb') as fin:
            _sent_tokenizer = pickle.load(fin)
    # Actual tokenization using the Punkt Model.
    return _sent_tokenizer.tokenize(text)


'''
def word_tokenize(text):
    """
    Treebank tokenizer.
    """
    global _word_tokenizer
    try:
        _word_tokenizer
    except NameError:
'''
