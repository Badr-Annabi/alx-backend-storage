#!/usr/bin/env python3
""" This is a Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def count_request(method: Callable) -> Callable:
    """Decorator for counting"""
    @wraps(method)
    def wrapper(url):
        """wrapper for decorator"""
        redis_.ince(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the html content from a url  """
    req = requests.get(url)
    return req.text
