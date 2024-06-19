#!/usr/bin/env python3

"""Initializes the Cache class with a Redis connection."""

from typing import Any, Callable, Optional, Union
import uuid
import redis
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A class decorator that counts the number of calls for a wrapped method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting functionality.
    """

    method_name = method.__qualname__  # Get qualified method name

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wraps the original method and increments the call count
        before execution.

        Args:
            self (Cache): The instance of the Cache class.
            *args: Arguments passed to the original method.
            **kwargs: Keyword arguments passed to the original method.

        Returns:
            Any: The return value of the original method.
        """

        self._redis.incr(method_name)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A class decorator to track the call history of a wrapped method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call history tracking functionality.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wraps the original method and stores input and output in Redis lists.

        Args:
            self (Cache): The instance of the Cache class.
            *args: Arguments passed to the original method.
            **kwargs: Keyword arguments passed to the original method
            (ignored for now).

        Returns:
            Any: The return value of the original method.
        """

        method_name = method.__qualname__  # Get qualified method name
        input_key = f"{method_name}:inputs"
        output_key = f"{method_name}:outputs"

        # Store input arguments (string)
        self._redis.rpush(input_key, str(args))
        result = str(method(self, *args, **kwargs))
        self._redis.rpush(output_key, str(result))  # Store output (string)

        return result

    return wrapper


def replay(fn: Callable):
    """
    Display the history of calls of a particular function.

    This function works with any callable that has been decorated with
    `call_history_decorator`.

    Args:
        fn (Callable): The function to display the call history for.
    """
    redis_client = redis.Redis()
    function_name = fn.__qualname__

    call_count = redis_client.get(function_name)
    call_count = call_count.decode('utf-8') if call_count else '0'

    print(f'{function_name} was called {call_count} times:')

    inputs_key = f"{function_name}:inputs"
    outputs_key = f"{function_name}:outputs"

    input_list = redis_client.lrange(inputs_key, 0, -1)
    output_list = redis_client.lrange(outputs_key, 0, -1)

    for input_data, output_data in zip(input_list, output_list):
        input_str = input_data.decode('utf-8') if input_data else ""
        output_str = output_data.decode('utf-8') if output_data else ""
        print(f'{function_name}(*{input_str}) -> {output_str}')


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

    @call_history
    @count_calls
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
