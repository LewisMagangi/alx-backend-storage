 #!/usr/bin/env python3

import redis
from functools import wraps
import uuid
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create keys for inputs and outputs
        inputs_key = f"{method.__module__}.{method.__qualname__}:inputs"
        outputs_key = f"{method.__module__}.{method.__qualname__}:outputs"

        # Normalize inputs and push to Redis
        self._redis.rpush(inputs_key, str(args))

        # Execute the original function
        output = method(*args, **kwargs)

        # Push output to Redis
        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port='6379', db=0)
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in a Redis server and returns a random gen key
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key, fn=None):
        """
        Retrieve a value from Redis,
        optionally applying a typecasting function.
        If the key does not exist, return None.
        If fn is provided, apply fn to the value before returning.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves a value from Redis and typecastes it to a string
        """
        return self.get(key, lambda value: value.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves a value from Redis and typecastes it to an interger
        """
        return self.get(key, lambda value: int(value.decode('utf-8')))
