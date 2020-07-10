import itertools
import os
import random
import re
import sys

try:
    from got.asts import consts
except ImportError:
    import consts


class ImmutableMixin(object):
    _inited = False

    def __init__(self):
        self._inited = True

    def __setattr__(self, key, value):
        if self._inited:
            raise NotImplementedError
        super().__setattr__(key, value)


class EnumMixin(object):
    def __iter__(self):
        for k, v in map(lambda x: (x, getattr(self, x)), dir(self)):
            if not k.startswith('_'):
                yield v


def tokenize(text):
    return re.findall(re.compile("[\w']+", re.U), text)


def itersubclasses(cls, _seen=None):

    if not isinstance(cls, type):
        raise TypeError(('itersubclasses must be called with '
                          'new-style classes, not %.100r') % cls)
    _seen = _seen or set()
    try:
        subs = cls.__subclasses__()
    except TypeError:
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
