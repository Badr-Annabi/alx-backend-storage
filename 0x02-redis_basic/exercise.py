#!/usr/bin/env python3
"""Creating a Cache Class"""
import redis
import uuid


class Cache():
    def __init__(self):
        """
        store an instance of the Redis client as
        a private variable named _redis (using redis.Redis())
        and flush the instance using flushdb
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data):
        """The method takes data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
