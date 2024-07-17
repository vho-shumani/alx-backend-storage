#!/usr/bin/env python3
"""exercise.py"""
import redis
from typing import Union
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
        self._redis.flushdb

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
