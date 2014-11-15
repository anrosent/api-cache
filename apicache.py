#!/usr/bin/env python3

import pickle, os.path

def read_cache(fn):
    try:
        return  pickle.load(fn)
    except Exception:
        return {}

class Cache(object):
    '''  '''
    def __init__(self, fn):
        if os.path.exists(fn):
            self.cachefile = open(fn, 'r+b')
        else:
            self.cachefile = open(fn, 'w+b')
        self.cache = read_cache(self.cachefile)

    def get(self, k):
        return self.cache[k]

    def contains(self, k):
        return k in self.cache

    # add to cache and persist
    def put(self, k, v):
        self.cache[k] = v

        # want to overwrite
        self.cachefile.seek(0)
        pickle.dump(self.cache, self.cachefile, -1)

    def close(self):
        self.cachefile.close()


def persist_memoize(cachefile):

    def decorator_func(f):
        cache = Cache(cachefile)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            if cache.contains(key):
                print("Cache hit: %s" % str(key))
                return cache.get(key)
            else:
                val = f(*args, **kwargs)
                cache.put(key, val)
                return val
        return wrapper
    return decorator_func

if __name__ == '__main__':
    @persist_memoize("cachefile")
    def tester(x):
        return 3*x

    v1 = tester(3)

