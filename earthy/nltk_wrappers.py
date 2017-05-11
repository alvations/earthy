# -*- coding: utf-8 -*-

import re
import os
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from nltk import download as nltk_download
from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.tag.perceptron import PerceptronTagger as AveragePerceptronTagger


class NLTKDownloader:
    def __init__(self, download_dir=None, xml_url=None):
        if xml_url:
            self._xml_url = xml_url
        else:
            self._nltk_data_url = u"https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/"
            self._xml_url = self._nltk_data_url + u"/index.xml"
        # Parse the XML file for available packages.
        self._packages_index, self._third_party = self.packages()
        # Set the default download directory if none is set.
        self._download_dir = download_dir if download_dir else self.default_download_dir()
        # Set the collection list.
        self._collections = {'all': self._packages_index,
                             'third_party': self._third_party
                             }

    def default_download_dir(self, download_dir=None):
        # Find the user's home directory.
        homedir = os.path.expanduser('~/')
        if homedir == '~/': # Sanity checks.
            raise ValueError("Could not find a default download directory")
        return os.path.join(homedir, 'earthy_data')

    def download(self, package_name, quiet=False):
        """
        For now, wrap around the NLTK's downloader.
        """
        # Check if user wants to download collections or a single package.
        if package_name in self._collections:
            to_download = self._collections[package_name]
        # Check if package name in the package index.
        elif package_name not in set(self._packages_index) | set(self._third_party):
            error_msg = "Package {} not found in index".format(package_name)
            raise ValueError(error_msg)
        else:
            to_download = [package_name]
        # Actual package downloading
        for pack in to_download:
            nltk_download(pack, download_dir=self._download_dir, quiet=quiet)

    def packages(self):
        """
        Parse XML file to locate packages.
        """
        xml = requests.get(self._xml_url).content
        soup = BeautifulSoup(xml, "html.parser")
        nltk_packages, third_party = defaultdict(dict), defaultdict(dict)
        for pack in soup.find_all('package'):
            package_attributes = pack.attrs
            name = package_attributes['id']
            # Keeps track of nltk_data packages vs third_party packages.
            if package_attributes['url'].startswith(self._nltk_data_url):
                nltk_packages[name] = package_attributes
            else:
                third_party[name] = package_attributes
        return nltk_packages, third_party


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
