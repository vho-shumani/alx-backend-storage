#!/usr/bin/env python3
"""
This module implements a get_page function with caching and access tracking.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_with_expiry(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            redis_client.incr(count_key)
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')
            result = func(url)
            redis_client.setex(cache_key, expiration_time, result)

            return result
        return wrapper
    return decorator


@cache_with_expiry(10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
