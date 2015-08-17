""" simple cache based on shelve
"""

import shelve
import time


def load_cache(cache_file):
    cache = shelve.open(cache_file)
    return cache


def read_key(cache, key, ttl):
    """ Reads value from cache, if doesnt exist or is older than ttl, raises KeyError
    """
    bibtex, timestamp = cache[key]

    if (timestamp + ttl) < time.time():
        raise KeyError("Cached entry is too old")
    else:
        return bibtex


def save_key(cache, key, value):
    cache[key] = (value, time.time())
