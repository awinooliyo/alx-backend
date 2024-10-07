#!/usr/bin/python3
""" LRU caching module """

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class that inherits from BaseCaching and implements
        an LRU caching system.
    """
    def __init__(self):
        """ Initialize the class and call the parent init """
        super().__init__()
        self.lru_order = []  # List to track the order of usage

    def put(self, key, item):
        """ Add an item to the cache using LRU algorithm """
        if key is not None and item is not None:
            if key in self.cache_data:
                # If key is already in cache, update the value and its usage
                self.cache_data[key] = item
                # Move the key to the most recent position in lru_order
                self.lru_order.remove(key)
                self.lru_order.append(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Cache is full, remove the least recently used key
                    lru_key = self.lru_order.pop(0)
                    del self.cache_data[lru_key]
                    print(f"DISCARD: {lru_key}")
                # Add new key and value to cache
                self.cache_data[key] = item
                self.lru_order.append(key)

    def get(self, key):
        """ Get an item by key from the cache and mark it as recently used """
        if key is None or key not in self.cache_data:
            return None
        # Move the key to the most recent position in lru_order
        self.lru_order.remove(key)
        self.lru_order.append(key)
        return self.cache_data[key]
