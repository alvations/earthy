# -*- coding: utf-8 -*-

import os
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from nltk import download as nltk_download


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
