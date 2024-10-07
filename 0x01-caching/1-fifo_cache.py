#!/usr/bin/python3
""" FIFO caching module """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class that inherits from BaseCaching and implements
        a FIFO caching system.
    """
    def __init__(self):
        """ Initialize the class and call the parent init """
        super().__init__()
        self.keys_order = []  # Keep track of the insertion order

    def put(self, key, item):
        """ Add an item to the cache using FIFO algorithm """
        if key is not None and item is not None:
            if key in self.cache_data:
                # If the key already exists, just update the value
                self.cache_data[key] = item
            else:
                # Add the new key and value to cache
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Cache is full, remove the first inserted key (FIFO)
                    first_key = self.keys_order.pop(0)
                    del self.cache_data[first_key]
                    print(f"DISCARD: {first_key}")

                # Add the key and value to the cache
                self.cache_data[key] = item
                self.keys_order.append(key)

    def get(self, key):
        """ Get an item by key from the cache """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
