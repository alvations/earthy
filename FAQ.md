How to download all NLTK data without `panlex_lite`?
====

Save it to your old `nltk_data` directory.

```python
import earthy
nltk_data_path = '/path/to/userhome/nltk_data/'
earthy.nltk_wrappers.download('all', nltk_data_path)
```

Downloads and save to the default `earthy_data` directory:

```python
import earthy
earthy.nltk_wrappers.download('all')
```


How to use default NLTK functions in `earthy`?
====

For now, these wrappers are supported:

 - `sent_tokenize`: Punkt sentence tokenizer
 - `word_tokenize`: NLTK improved treebank word tokenizer
 - `pos_tag`: @honnibal's averaged perceptron POS tagger.


```python
>>> from earthy.nltk_wrappers import sent_tokenize, word_tokenize, pos_tag

>>> s = "Earthy is a library for natural language processing in Python. Earthy is built on the not-so-latest research (for now), and it is a researchware that's very use-able for the industry."

>>> [pos_tag(word_tokenize(sent)) for sent in sent_tokenize(s)]
[[('Earthy', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('library', 'NN'), ('for', 'IN'), ('natural', 'JJ'), ('language', 'NN'), ('processing', 'NN'), ('in', 'IN'), ('Python', 'NNP'), ('.', '.')], [('Earthy', 'NNP'), ('is', 'VBZ'), ('built', 'VBN'), ('on', 'IN'), ('the', 'DT'), ('not-so-latest', 'JJ'), ('research', 'NN'), ('(', '('), ('for', 'IN'), ('now', 'RB'), (')', ')'), (',', ','), ('and', 'CC'), ('it', 'PRP'), ('is', 'VBZ'), ('a', 'DT'), ('researchware', 'NN'), ('that', 'WDT'), ("'s", 'VBZ'), ('very', 'RB'), ('use-able', 'JJ'), ('for', 'IN'), ('the', 'DT'), ('industry', 'NN'), ('.', '.')]]
```

Other the classic default functions in NLTK, here's a few more that `earthy` wraps:

  - `wordnet_lemmatize`: wraps around the `nltk.stem.WordNetLemmatizer().lemmatize` function.
  - `snowball_stem`: wraps around the `nltk.stem.SnowballStemmer().stem` function.
  - `porter_stem`: wraps around the `nltk.stem.SnowballStemmer('porter').stem` function.
  - `pywsd_lemmatize` and `lemmatize_sent` are from https://gist.github.com/alvations/07758d02412d928414bb


```python
>>> from earthy.nltk_wrappers import *
# Stemmers.
>>> porter_stem('running')
u'run'
>>> snowball_stem('running')
u'run'
# Lemmatizers.
>>> wordnet_lemmatize('running', 'v')
u'run'
>>> wordnet_lemmatize('running', 'n')
'running'
>>> pywsd_lemmatize('running')
'running'
>>> pywsd_lemmatize('running', 'v')
u'run'
>>> wordnet_lemmatize('lessoning')
'lessoning'
>>> pywsd_lemmatize('lessoning', apply_stemming=True)
u'lesson'
>>> lemmatize_sents('This is a foo bar sentence.')
[('This', 'This', 'DT'), ('is', 'be', 'VBZ'), ('a', 'a', 'DT'), ('foo', 'foo', 'JJ'), ('bar', 'bar', 'NN'), ('sentence', 'sentence', 'NN'), ('.', '.', '.')]
```
