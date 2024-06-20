#!/usr/bin/env python3
""" Class Cache """


import redis
from typing import Union, Any, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator to count the number of calls to a method  """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and
    outputs"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """doc doc class"""
        self._redis.rpush(input_key, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    # sourcery skip: use-fstring-for-concatenation, use-fstring-for-formatting
    """
    This func replays the history of a function
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for input_, output_ in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, input_.decode('utf-8'),
                                     output_.decode('utf-8')))


class Cache:
    """ Class Cache """

    def __init__(self) -> None:
        """ init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store method """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ get a key and convert it to a desired format"""
        value = self._redis.get(key)
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ gets a value and convert it to a string"""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ gets a value and convert it to a string"""
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
