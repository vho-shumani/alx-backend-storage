#!/usr/bin/env python3
"""exercise.py"""
import redis
from typing import Union, Callable, Optional
import uuid


class Cache():
    """
    Class initializes a Redis client and offers methods to store data
    """
    def __init__(self):
        """
        Creates a Redis client and flushes database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        Args:
            data(str, byte, int, float): data to be stored.

        Return:
            str: return generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis using given key
        and appy optional conversation method

        Args:
            key(str): the key to retrieve
            fn(optional[callable]): optional callable to
            convert the retieve data

        Return:
            The retrieved data, converted, or None if its not it Redis
        """
        data = self._redis.get(key)
        if not data:
            return None
        if fn:
            return fn(data)
        return data

        def get_str(self, key: str) -> str:
            """
            Retrieve string

            Args:
                key(str): key to retieve

            return:
                return retrieved string data, or None if it doesnt exists.
            """
            data = self.get(key)
            if data:
                return data.decode("utf-8")
            else:
                return None

        def get_int(self, key: str) -> int:
            """
            Retrieves interger

            Args:
                key(str): key to retrieve.

            return:
                retrieved interger, or None if it doesnt exists.
            """
            data = self.get(key)
            if data:
                return int(data)
            else:
                return None
