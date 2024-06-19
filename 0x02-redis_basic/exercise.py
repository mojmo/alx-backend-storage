#!/usr/bin/env python3

"""Initializes the Cache class with a Redis connection."""

from typing import Union
import uuid
import redis


class Cache:
    """
    A class to interact with Redis as a simple cache.

    This class provides methods to store and retrieve data from Redis,
    offering a convenient way to cache data in your Python applications.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client for interacting
            with the Redis server.
    """

    def __init__(self):
        """
        Initializes the Cache class with a Redis connection.
        """

        self._redis = redis.Redis()
        self._redis.flushdb() # Flush the cache on initialization

    def store (self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in Redis and returns a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be cached.

        Returns:
            str: The randomly generated key used to store the data.
        """

        key = str(uuid.uuid4()) # Generate a unique key as a string
        self._redis.set(key, data)
        return key
