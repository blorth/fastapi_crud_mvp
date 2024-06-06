from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes TTL
