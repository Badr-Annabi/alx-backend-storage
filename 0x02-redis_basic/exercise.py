#!/usr/bin/env python3
"""Creating a Cache Class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache():
    def __init__(self):
        """
        store an instance of the Redis client as
        a private variable named _redis (using redis.Redis())
        and flush the instance using flushdb
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """The method takes data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get sata from cache"""
        value = self._redis.get(key)
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Get a string from the cache """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """ Get an int from the cache  """
        return self.get(key, fn=int)
