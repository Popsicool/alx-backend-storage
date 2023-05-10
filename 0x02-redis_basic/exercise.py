#!/usr/bin/env python3
'''
Writing strings to Redis
'''
import redis
from uuid import uuid4
import requests
from typing import Union, Optional, Callable
from functools import wraps
rc = redis.Redis()


def count_history(method: Callable) -> Callable:
    '''
    call history
    '''
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    counts call
    """
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapped
        """
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper


def replay(method: Callable):
    '''
    replay method
    '''
    m_key = method.__qualname__
    inputs = m_key + ":inputs"
    outputs = m_key + ":outputs"
    redis = method.__self__._redis
    cnt = redis.get(m_key).decode("utf-8")
    print("{} was called {} times:".format(m_key, cnt))
    AllInp = redis.lrange(inputs, 0, -1)
    AllOut = redis.lrange(outputs, 0, -1)
    allData = list(zip(AllInp, AllOut))
    for k, v in allData:
        key = k.decode("utf-8")
        value = v.decode("utf-8")
        print("{}(*{}) -> {}".format(m_key, key, value))


class Cache:
    '''
    store an instance of the Redis client as a private variable
    '''
    def __init__(self) -> None:
        '''initialize  the class'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[bytes, str, float, int]) -> str:
        '''
        store the input data in Redis using the random key
        '''
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[bytes, str, float, int]:
        '''
        get data
        '''
        value = self._redis.get(key)
        if (fn):
            return fn(value)
        return value

    def get_str(self, data: str) -> str:
        '''
        class method to decode to str
        '''
        return data.decode('utf-8')

    def get_int(self, data: str) -> int:
        '''
        class method to decode to int
        '''
        return int(data)
