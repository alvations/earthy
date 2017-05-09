How to download all NLTK data without `panlex_lite`?
====

Save it to your old `nltk_data` directory.

```python
import earthy
nltk_data_path = '/path/to/userhome/nltk_data/'
earthy.download('all', nltk_data_path)
```

Downloads and save to the default `earthy_data` directory:

```python
import earthy
earthy.download('all')
```
