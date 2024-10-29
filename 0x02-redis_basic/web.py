#!/usr/bin/env python3
"""Module to fetch and cache web pages using Redis with request tracking and expiration"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client
cache = redis.Redis()


def cache_page(expiration: int = 10) -> Callable:
    """Decorator to cache page content and track access count"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Track the URL access count
            cache_key_count = f"count:{url}"
            cache.incr(cache_key_count)

            # Attempt to retrieve cached content
            cache_key_content = f"cached:{url}"
            cached_content = cache.get(cache_key_content)

            if cached_content:
                return cached_content.decode('utf-8')

            # Fetch and cache content if not cached
            content = func(url)
            cache.setex(cache_key_content, expiration, content)
            return content

        return wrapper
    return decorator


@cache_page()
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it"""
    response = requests.get(url)
    return response.text


# Sample usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com"
    print(get_page(url))

