#!/usr/bin/python3
""" LFU Caching Module """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that implements a LFU caching system.
        If multiple keys have the same frequency, use the LRU algorithm.
    """

    def __init__(self):
        """ Initialize class instance. """
        super().__init__()
        self.freq = {}
        self.lru_order = {}

    def put(self, key, item):
        """ Add an item in the cache using LFU algorithm """
        if key is None or item is None:
            return

        # If key already exists in cache, update its value and usage
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.lru_order[key] = len(self.lru_order)
        else:
            # If cache is full, remove the least frequently used item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu_key = self.get_lfu_key()
                if lfu_key is not None:
                    del self.cache_data[lfu_key]
                    del self.freq[lfu_key]
                    del self.lru_order[lfu_key]
                    print(f"DISCARD: {lfu_key}")

            # Add the new key and item to cache
            self.cache_data[key] = item
            self.freq[key] = 1
            self.lru_order[key] = len(self.lru_order)

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is None or key not in self.cache_data:
            return None
        # Update frequency and LRU order
        self.freq[key] += 1
        self.lru_order[key] = len(self.lru_order)
        return self.cache_data[key]

    def get_lfu_key(self):
        """ Find the least frequently used (LFU) key. Break ties with LRU. """
        if not self.cache_data:
            return None

        # Find the minimum frequency
        min_freq = min(self.freq.values())

        # Gather keys that have the minimum frequency
        min_freq_keys = [k for k, v in self.freq.items() if v == min_freq]

        # If there are multiple keys with the same frequency, apply LRU policy
        if len(min_freq_keys) == 1:
            return min_freq_keys[0]

        # Select the least recently used key among the least frequently used
        return min(min_freq_keys, key=lambda k: self.lru_order[k])
