# -*- coding: utf-8 -*-

from setuptools import setup

requires = ['gensim', 'scikit-learn', 'nltk',
            'six', 'beautifulsoup4', 'requests',
            'numpy', 'pandas']

setup(
  name='earthy',
  packages=['earthy'],
  version='0.0.5',
  description='',
  install_requires=requires,
  author='Mere Mortal',
  license='MIT',
  url='https://github.com/alvations/earthy',
  #download_url='https://github.com/alvations/earthy/tarball/0.0.2',
  keywords=['natural language processing', 'computational linguistics'],
  classifiers=[],
)
