#!/usr/bin/env python3

"""Initializes the Cache class with a Redis connection."""

from typing import Any, Callable, Optional, Union
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
        self._redis.flushdb()  # Flush the cache on initialization

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in Redis and returns a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be cached.

        Returns:
            str: The randomly generated key used to store the data.
        """

        key = str(uuid.uuid4())  # Generate a unique key as a string
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Retrieves data from Redis for the given key and optionally applies
        a conversion function.

        Args:
            key (str): The key used to store the data in Redis.
            fn (Optional[Callable], optional): A callable function
                to convert the retrieved data (bytes) to the desired format.
                Defaults to None, preserving the original Redis.get behavior if
                the key does not exist.

        Returns:
            Any: The retrieved data in the desired format (string, int, etc.),
                or None if the key does not exist.
        """

        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data from Redis for the given key, assuming it's stored
        as a string and converts it to a decoded UTF-8 string.

        Args:
            key (str): The key used to store the data in Redis.

        Returns:
            Optional[str]: The retrieved data as a decoded string, or None
            if the key does not exist or the data cannot be decoded as UTF-8.
        """

        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis for the given key, assuming it's stored
        as an integer and converts it to an integer type.

        Args:
            key (str): The key used to store the data in Redis.

        Returns:
            Optional[int]: The retrieved data as an integer, or None if the
            key does not exist or the data cannot be converted to an integer.
        """

        try:
            return int(self.get(key))
        except (ValueError, TypeError):
            return None


if __name__ == '__main__':
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value