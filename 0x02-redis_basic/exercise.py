#!/usr/bin/env python3
"""Redis cache implementation with call history replay"""
import redis
from functools import wraps
import uuid
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """Decorator to count method calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls for a particular function"""
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    # Get the number of calls
    calls = redis_instance.get(method_name)
    calls = int(calls) if calls else 0

    print(f"{method_name} was called {calls} times:")

    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    for inp, outp in zip(inputs, outputs):
        # Convert bytes to string and format properly
        input_str = inp.decode('utf-8').strip('()')
        output_str = outp.decode('utf-8')
        print(f"{method_name}(*({input_str},)) -> {output_str}")


class Cache:
    """Cache class for Redis operations"""

    def __init__(self):
        """Initialize Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with random key"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Get data from Redis with optional type conversion"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key: str) -> Optional[str]:
        """Get string data from Redis"""
        return self.get(key, lambda value: value.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Get integer data from Redis"""
        return self.get(key, lambda value: int(value.decode('utf-8')))
