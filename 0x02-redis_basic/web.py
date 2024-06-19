#!/usr/bin/env python3

"""Obtain the HTML content of a particular URL and returns it."""

import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_page(expiration: int = 10):
    """
    Decorator to cache the HTML content of a URL and track the
    number of times it was accessed.
    """
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(url: str) -> str:
            # Increment the count for the URL
            count_key = f"count:{url}"
            redis_client.incr(count_key)

            # Check if the URL content is already cached
            cache_key = f"cache:{url}"
            cached_content = redis_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # Get the HTML content from the URL
            html_content = fn(url)

            # Cache the content with an expiration time
            redis_client.setex(cache_key, expiration, html_content)
            return html_content
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text
