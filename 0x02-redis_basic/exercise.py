#!/usr/bin/env python3

import uuid
import redis
from typing import Union, Callable
"""
Create a Cache class. In the __init__ method, store an
Type-annotate store correctly. Remember that data can be a str,
bytes, int or float.
"""


class Cache:
    def __init__(self):
        """
        instance of the Redis client as a private variable named _redis
        (using redis.Redis()) and flush the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Create a store method that takes a data argument and returns a
        string. The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the
        key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fh: Callable=None):
        """
        create a get method that take a key string argument and an
        optional Callable argument named fn. This callable will be
        used to convert the data back to the desired format.

        Remember to conserve the original Redis.get behavior if the
        key does not exist.
        """
        if self._redis.exists(key):
            data = self._redis.get(key)
            if fh:
                return fh(data)
            return data
        return None

    def get_str(self, key: str):
        """implement 2 new methods: get_str and get_int that will
        automatically parametrize Cache.get with the correct
        conversion function."""
        return self.get(key, fh=str)

    def get_int(self, key: int):
        """return int"""
        return self.get(key, fh=int)
