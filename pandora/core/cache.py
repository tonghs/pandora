import hashlib

from flask import g, request
from flask_caching import Cache


def is_logined():
    return bool(g.me)


def common_cache_key():
    params = dict(request.values.items())
    params.pop('sk', None)
    params.pop('api_sign', None)
    args_as_sorted_tuple = tuple(
        sorted(
            (pair for pair in params.items())
        )
    )
    args_as_bytes = str(args_as_sorted_tuple).encode()
    hashed_args = str(hashlib.md5(args_as_bytes).hexdigest())
    cache_key = request.path + hashed_args
    return cache_key


class PandoraCache(Cache):

    def cache_for_anonymous(self, timeout=5 * 60):
        return self.cached(timeout=timeout, unless=is_logined, key_prefix=common_cache_key)


ONE_MINUTE = 60
ONE_HOUR = 60 * 60
ONE_DAY = 24 * 60 * 60
