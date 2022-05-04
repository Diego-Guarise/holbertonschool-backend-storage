#!/usr/bin/env python3

import uuid
import redis
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

    def store(self, data):
        """
        Create a store method that takes a data argument and returns a
        string. The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the
        key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
