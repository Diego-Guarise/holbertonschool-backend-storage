#!/usr/bin/env python3
"""
Redis caching module
"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    asd
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        method_name = method.__qualname__
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    input and output list key
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        method_name = method.__qualname__
        data = str(args)
        method_result = method(self, data)
        self._redis.rpush("{}:inputs".format(method_name), data)
        self._redis.rpush("{}:outputs".format(method_name), method_result)
        return method_result
    return wrapper


def replay(func: Callable):
    """
    display the history
    """
    r = redis.Redis()
    method_name = func.__qualname__
    inputs = r.lrange("{}:inputs".format(method_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(method_name), 0, -1)
    call_number = len(inputs)
    times_str = 'times'
    if call_number == 1:
        times_str = 'time'
    msg = '{} was called {} {}:'.format(method_name, call_number, times_str)
    print(msg)
    for k, v in zip(inputs, outputs):
        msg = '{}(*{}) -> {}'.format(
            method_name,
            k.decode('utf8'),
            v.decode('utf8')
        )
        print(msg)


class Cache:
    """
    class
    """

    def __init__(self):
        """
        Initialization
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ returns the random key """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(
            self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        returns the key's value
        """
        result = self._redis.get(key)
        if fn:
            return fn(result)
        return result

    def get_str(self, key) -> str:
        """
        returns key
        """
        return get(key, str)

    def get_int(self, key) -> int:
        """
        Returns key
        """
        return get(key, int)