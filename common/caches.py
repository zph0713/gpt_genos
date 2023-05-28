import redis
import json
from common.base import load_config



class RedisCache(object):
    # Connect to Redis 
    def __init__(self):
        self.config = load_config()
        self.cache_config = self.config['cache']
        self.cache = redis.Redis.from_url(self.cache_config)


    # Set a key
    def set(self, key, value):
        if isinstance(value,dict):
            value = json.dumps(value)
        self.cache.set(key, value)

    # Set a key with expiration
    def setex(self, key, value, time):
        if isinstance(value,dict):
            value = json.dumps(value)
        self.cache.setex(key, time, value)

    # Get a key
    def get(self, key):
        value = self.cache.get(key)
        if value:
            try:
                value = json.loads(value)
            except:
                pass
        return value
    
    # Delete a key
    def delete(self, key):
        self.cache.delete(key)

    # Clear all keys
    def clear(self):
        self.cache.flushall()

    # Get all keys
    def get_all(self):
        keys = self.cache.keys()
        return keys
    