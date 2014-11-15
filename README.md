apicache.py
===

Memoization is a great technique for preventing repeated computation of the same expression. I find this persistent memoization useful when prototyping scripts that deal with web APIs that may be slow or rate-limited and require internet connectivity. This makes the edit-run-debug loop a lot snappier when dealing with those kinds of services with minimal footprint in your code - just wrap your expensive API request with the provided function decorator ```persist_memoize```.

Usage
---
Pretty simple, just decorate any function as follows

    from apicache import persist_memoize

    @persist_memoize('foo.cache')
    def foo(url):
        return process_api_response(url)

