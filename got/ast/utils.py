import itertools
import os
import random
import re
import sys

import consts


class ImmutableMixin(object):
    _inited = False

    def __init__(self):
        self._inited = True

    def __setattr__(self, key, value):
        if self._inited:
            raise NotImplementedError
        super(ImmutableMixin, self).__setattr__(key, value)


class EnumMixin(object):
    def __iter__(self):
        for k, v in map(lambda x: (x, getattr(self, x)), dir(self)):
            if not k.startswith('_'):
                yield v


def prepare_text(text):
    text = text.upper()
    return text


def tokenize(text):
    return re.findall(re.compile("[\w']+", re.U), text)


def tokenize_and_filter(text, min_word_length=3, stopwords=None):
    tokens = tokenize(text)
    stopwords = stopwords or set(word.upper() for word in nltk_stopwords.words("english"))
    return [token for token in tokens
            if len(token) >= min_word_length and token not in stopwords]


def text_to_strings_collection(text, words=3):
    
    text = prepare_text(text)
    strings_collection = tokenize(text)
    strings_collection = [s for s in strings_collection if len(s) > 2 and not s.isdigit()]
        
    i = 0
    strings_collection_grouped = []
    while i < len(strings_collection):
        group = ''
        for j in range(words):
            if i + j < len(strings_collection):
                group += strings_collection[i+j]
        strings_collection_grouped.append(group)
        i += words

    if not strings_collection_grouped:
        strings_collection_grouped = [" "]
        
    return strings_collection_grouped


def text_collection_to_string_collection(text_collection, words=3):
    return flatten([text_to_strings_collection(text) for text in text_collection])


def random_string(length):
    string = "".join([chr(ord("A") + random.randint(0, 25)) for _ in range(length - 2)])
    return string


def flatten(lst):
    return list(itertools.chain.from_iterable(lst))


def output_is_redirected():
    return os.fstat(0) != os.fstat(1)


def itersubclasses(cls, _seen=None):

    if not isinstance(cls, type):
        raise TypeError(('itersubclasses must be called with '
                          'new-style classes, not %.100r') % cls)
    _seen = _seen or set()
    try:
        subs = cls.__subclasses__()
    except TypeError:   # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub_ in itersubclasses(sub, _seen):
                yield sub_


def import_modules_from_package(package):
    path = [os.path.dirname(__file__), '..'] + package.split('.')
    path = os.path.join(*path)
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.startswith('__') or not filename.endswith('.py'):
                continue
            new_package = ".".join(root.split(os.sep)).split("....")[1]
            module_name = '%s.%s' % (new_package, filename[:-3])
            if module_name not in sys.modules:
                __import__(module_name)


def index(array, key, start=0):
    i = start
    while array[i] != key:
        i += 1
    return i


def match_strings(str1, str2):
    """
    Returns the largest index i such that str1[:i] == str2[:i]
    
    """
    i = 0
    min_len = len(str1) if len(str1) < len(str2) else len(str2)
    while i < min_len and str1[i] == str2[i]: i += 1
    return i


def make_unique_endings(strings_collection):
    """
    Make each string in the collection end with a unique character.
    Essential for correct builiding of a generalized annotated suffix tree.
    Returns the updated strings collection, encoded in Unicode.

    max strings_collection ~ 1.100.000
    
    """
    res = []
    for i in range(len(strings_collection)):
        hex_code = hex(consts.String.UNICODE_SPECIAL_SYMBOLS_START+i)
        hex_code = r"\U" + "0" * (8 - len(hex_code) + 2) + hex_code[2:]
        res.append(strings_collection[i] + hex_code.encode('latin-1').decode("unicode-escape"))
    return res
