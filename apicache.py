'''
    Module providing persistent memoization via a function decorator
    `persistent_memoize`. Useful in the development loop for scripts using
    external APIs to enable testing and iteration without worrying about
    internet connectivity or overloading the APIs.
'''
import pickle
import os.path


def read_cache(filename):
    '''
        Deserializes the persistent memoization cache in the given file
    '''
    try:
        return pickle.load(filename)
    except EOFError:
        return {}


class Cache(object):
    '''
        Persistent key-value store; all writes trigger overwrite of the cache
        on-disk
    '''
    def __init__(self, filename):
        if os.path.exists(filename):
            self.cachefile = open(filename, 'r+b')
        else:
            self.cachefile = open(filename, 'w+b')
        self.cache = read_cache(self.cachefile)

    def get(self, k):
        '''
            Retrieves value for key k in cache
        '''
        return self.cache[k]

    def contains(self, k):
        '''
            Returns True if the cache contains an entry with key k,
            False otherwise
        '''
        return k in self.cache

    def put(self, k, val):
        '''
            Adds the entry (k, v) to the cache, triggering an update of the
            cache on-disk
        '''

        self.cache[k] = val

        # Overwrite entire cache file with current cache contents
        self.cachefile.seek(0)
        pickle.dump(self.cache, self.cachefile, -1)

    def close(self):
        '''
            Releases file handle on pickled cache file
        '''
        self.cachefile.close()


def persist_memoize(cachefile):
    '''
        Decorator wrapping functions with persistent memoization using
        a pickled dictionary in the given file

        Test:
            NOTE: running this leaves a file cachefile in cwd

        >>> @persist_memoize("cachefile")
        ... def tester(x):
        ...     print('func eval')
        ...     return 3*x
        >>> tester(3)
        func eval
        9
        >>> tester(3)
        9
    '''
    # Close over cache and argument function to wrap
    def decorator_func(func):
        cache = Cache(cachefile)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            if cache.contains(key):
                return cache.get(key)
            else:
                val = func(*args, **kwargs)
                cache.put(key, val)
                return val
        return wrapper
    return decorator_func
