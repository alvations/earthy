# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requires = ['gensim', 'scikit-learn', 'nltk',
            'six', 'beautifulsoup4', 'requests',
            'numpy', 'pandas']

setup(
  name='earthy',
  packages=find_packages(),
  version='0.0.11',
  description='',
  install_requires=requires,
  author='Mere Mortal',
  license='MIT',
  url='https://github.com/alvations/earthy',
  #download_url='https://github.com/alvations/earthy/tarball/0.0.2',
  keywords=['natural language processing', 'computational linguistics'],
  classifiers=[],
)
