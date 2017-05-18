# -*- coding: utf-8 -*-

import re
import pickle
from itertools import chain

from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.tag.perceptron import PerceptronTagger
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.corpus import wordnet as wn

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


def pos_tag_sents(list_of_tokenized_text):
    """
    Averaged perceptron tagger from NLTK (originally from @honnibal)
    """
    global _nltk_pos_tagger
    try:
        _nltk_pos_tagger
    except NameError:
        _nltk_pos_tagger = PerceptronTagger()
        # Checks that the punkt tokenizer model was previously downloaded.
        download('averaged_perceptron_tagger', quiet=True)
    return _nltk_pos_tagger.tag_sents(list_of_tokenized_text)


def pos_tag(tokenized_text):
    """
    Averaged perceptron tagger from NLTK (originally from @honnibal)
    """
    return pos_tag_sents([tokenized_text])[0]


def porter_stem(word):
    return snowball_stem(word, 'porter')


def snowball_stem(word, lang='english'):
    global _nltk_snowball_stemmer
    try:
        _nltk_snowball_stemmer
    except NameError:
        available_languages = ['danish', 'dutch', 'english', 'finnish', 'french',
                               'german', 'german2', 'hungarian', 'italian',
                               'kraaij_pohlmann', 'lovins', 'norwegian',
                               'porter', 'portuguese', 'romanian', 'russian',
                               'spanish', 'swedish', 'turkish']
        assert lang in available_languages, "Snowball Stemmer for {} not available".format(lang)
        # Checks that the snowball data was previously downloaded.
        download('snowball_data', quiet=True)
        _nltk_snowball_stemmer = SnowballStemmer(lang)
    return _nltk_snowball_stemmer.stem(word)


def penn2morphy(penntag, default_tag='n'):
    global morphy_tag
    try:
        morphy_tag
    except NameError:
        morphy_tag = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r',
                      'n':'n', 'a':'a', 's':'s', 'v':'v', 'r':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return default_tag


def wordnet_lemmatize(word, pos='n'):
    global _nltk_wordnet_lemmatizer
    try:
        _nltk_wordnet_lemmatizer
    except NameError:
        _nltk_wordnet_lemmatizer = WordNetLemmatizer()
    return _nltk_wordnet_lemmatizer.lemmatize(word, penn2morphy(pos))



def pywsd_lemmatize(word, pos='n', apply_stemming=False):
    lemma = wordnet_lemmatize(word, penn2morphy(pos))
    if wn.synsets(lemma):
        return lemma
    else:
        if apply_stemming:
            stem = snowball_stem(word)
            return stem if wn.synsets(stem) else word
        else:
            return word


def lemmatize_sent(text, apply_stemming=True):
    return [(word, pywsd_lemmatize(word, pos, apply_stemming), pos)
            for word, pos in pos_tag(word_tokenize(text))]


lemmatize_sent('This is a foo bar sentence.')
