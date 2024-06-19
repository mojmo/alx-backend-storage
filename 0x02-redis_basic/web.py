#!/usr/bin/env python3

"""Obtain the HTML content of a particular URL and returns it."""

import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_page(fn: Callable) -> Callable:
    """
    Decorator to cache the HTML content of a URL and track the
    number of times it was accessed.
    """

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wraps the original method"""

        # Increment the count for the URL
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        # Check if the URL content is already cached
        cache_key = f"cached:{url}"
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Get the HTML content from the URL
        html_content = fn(url)

        # Cache the content with an expiration time
        redis_client.setex(cache_key, 10, html_content)
        return html_content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL."""
    response = requests.get(url)
    return response.text
