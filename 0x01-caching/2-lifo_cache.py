#!/usr/bin/python3
""" LIFO caching module """

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class that inherits from BaseCaching and implements
        a LIFO caching system.
    """
    def __init__(self):
        """ Initialize the class and call the parent init """
        super().__init__()
        self.last_key = None  # Track the last inserted key

    def put(self, key, item):
        """ Add an item to the cache using LIFO algorithm """
        if key is not None and item is not None:
            # Add or update the cache with the new key and value
            if key in self.cache_data:
                self.cache_data[key] = item
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Discard the last added key (LIFO)
                    if self.last_key:
                        del self.cache_data[self.last_key]
                        print(f"DISCARD: {self.last_key}")

                # Update cache with new key and value
                self.cache_data[key] = item
                self.last_key = key  # Update last inserted key

    def get(self, key):
        """ Get an item by key from the cache """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
