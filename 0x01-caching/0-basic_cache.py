#!/usr/bin/python3
""" Basic caching module """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class that inherits from BaseCaching and implements
        a basic caching system without limit.
    """
    def put(self, key, item):
        """ Assign the item value to the key in the cache """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Return the value linked to the key in the cache """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
