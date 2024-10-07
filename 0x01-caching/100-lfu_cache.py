#!/usr/bin/python3
""" LFU Caching Module """

from base_caching import BaseCaching

class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching and implements
        a Least Frequently Used (LFU) caching system with LRU as a tie-breaker.
    """
    def __init__(self):
        """ Initialize the class and call the parent init """
        super().__init__()
        self.freq = {}      # Track how often items are accessed
        self.lru_order = {}  # Track the order of access for LRU resolution

    def put(self, key, item):
        """ Add an item to the cache using LFU algorithm """
        if key is None or item is None:
            return

        # If the key already exists, update the value and usage
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.lru_order[key] = len(self.lru_order)  # Update to most recent
        else:
            # If the cache is full, evict the least frequently used item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the LFU key, and resolve ties using LRU
                lfu_key = self.get_lfu_key()
                if lfu_key is not None:
                    del self.cache_data[lfu_key]
                    del self.freq[lfu_key]
                    del self.lru_order[lfu_key]
                    print(f"DISCARD: {lfu_key}")

            # Add the new key and update frequency and order
            self.cache_data[key] = item
            self.freq[key] = 1
            self.lru_order[key] = len(self.lru_order)

    def get(self, key):
        """ Get an item by key from the cache and update its frequency """
        if key is None or key not in self.cache_data:
            return None
        # Update frequency and order
        self.freq[key] += 1
        self.lru_order[key] = len(self.lru_order)  # Update to most recent
        return self.cache_data[key]

    def get_lfu_key(self):
        """ Helper method to get the Least Frequently Used (LFU) key """
        if not self.cache_data:
            return None

        # Get the minimum frequency from freq dictionary
        min_freq = min(self.freq.values())

        # Get all keys that have the minimum frequency
        min_freq_keys = [k for k, v in self.freq.items() if v == min_freq]

        # Use LRU policy among items with the same frequency
        if len(min_freq_keys) == 1:
            return min_freq_keys[0]

        # Return the least recently used key (based on lru_order)
        lru_key = min(min_freq_keys, key=lambda k: self.lru_order[k])
        return lru_key
