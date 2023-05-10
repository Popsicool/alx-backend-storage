#!/usr/bin/env python3
'''
Implementing an expiring web cache and tracker
'''

import redis
import requests
redis_count = redis.Redis()
count = 0


def get_page(url: str) -> str:
    '''
    get page
    '''
    redis_count.set(f"cached:{url}", count)
    response = requests.get(url)
    redis_count.incr(f"count:{url}")
    redis_count.setex(f"cached:{url}", 10,
                      redis_count.get(f"cached:{url}"))
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
