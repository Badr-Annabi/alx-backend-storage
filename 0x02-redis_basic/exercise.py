#!/usr/bin/env python3
"""Creating a Cache Class"""
import redis
import uuid
from typing import Union, Callable

class Cache():
    def __init__(self):
        """
        store an instance of the Redis client as
        a private variable named _redis (using redis.Redis())
        and flush the instance using flushdb
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """The method takes data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get sata from cache"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Get a string from the cache """
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ Get an int from the cache  """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
