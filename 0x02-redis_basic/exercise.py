#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port='6379', db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in a Redis server and returns a random gen key
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def fn(self, key) -> str:
        """
        Retrieves data from the Redis server and decodes it if it's of type bytes
        """
        data = self._redis.get(key)
        if type(data) == bytes:
            data = data.decode('utf-8')
            return data
        return data
    
    def get(self, key:str, fn=None):
        """
        Retrieve a value from Redis, optionally applying a transformation function.
        """
        value = self._redis.store.get(key)
        if fn and callable(fn):
            return fn(value)
        return value

    def get_str(self, key:str) -> Union[str, None]:
        """
        Retrieves a value from Redis and typecastes it to a string
        """
        return self.get(key, lambda value: value.decode('utf-8') if type(value) == bytes else str(value))

    def get_int(self, key):
        """
        Retrieves a value from Redis and typecastes it to an interger
        """
        return self.get(key, lambda value: value.decode('utf-8') if type(value) == bytes else int(value))
