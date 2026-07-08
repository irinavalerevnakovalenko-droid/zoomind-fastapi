from collections.abc import Callable
from functools import wraps


KeyBuilder = Callable[..., str]

def cached(
    *,
    ttl: int,
    key_builder: KeyBuilder,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = kwargs.get('cache')

            if cache is None:
                return await func(*args, **kwargs)

            cache_key = key_builder(*args, **kwargs)
            cached_value = await cache.get(cache_key)

            if cached_value is not None:
                return cached_value

            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator