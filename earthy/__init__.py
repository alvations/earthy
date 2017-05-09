# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

from earthy.downloader import Downloader


def download(name, download_dir=None, xml_url=None):
    # Create the Downloader object.
    global _downloader
    _downloader = Downloader(download_dir, xml_url)
    _downloader.download(name)
