#!/usr/bin/env python3
"""exercise.py"""
import redis
from typing import Union, Callable, Optional, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """
        Wrapper function that increments the
        call count and calls the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.
    """
    red = redis.Redis()
    method_name = method.__qualname__
    inputs = red.lrange(f"{method_name}:inputs", 0, -1)
    outputs = red.lrange(f"{method_name}:outputs", 0, -1)
    calls_count = len(inputs)

    print(f"{method_name} was called {calls_count} times:")

    for inp, out in zip(inputs, outputs):
        input_str = inp.decode('utf-8')
        output_str = out.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


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

    @call_history
    @count_calls
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
