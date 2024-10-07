#!/usr/bin/python3
""" MRU caching module """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class that inherits from BaseCaching and implements
        an MRU caching system.
    """
    def __init__(self):
        """ Initialize the class and call the parent init """
        super().__init__()
        self.mru_order = []  # List to track the order of usage

    def put(self, key, item):
        """ Add an item to the cache using MRU algorithm """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update value and move key to most recent position
                self.cache_data[key] = item
                self.mru_order.remove(key)
                self.mru_order.append(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Cache is full, remove the most recently used key
                    mru_key = self.mru_order.pop()
                    del self.cache_data[mru_key]
                    print(f"DISCARD: {mru_key}")

                # Add new key and value to cache
                self.cache_data[key] = item
                self.mru_order.append(key)

    def get(self, key):
        """ Get an item by key from the cache """
        if key is None or key not in self.cache_data:
            return None
        # Move the key to the most recent position in mru_order
        self.mru_order.remove(key)
        self.mru_order.append(key)
        return self.cache_data[key]
