import datetime
import decimal

from flask.json import JSONEncoder
from raven.contrib.flask import Sentry

from pandora import config
from pandora.core.cache import PandoraCache
from pandora.core.db import MyRetryDB


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)


db = MyRetryDB(
    config.DB_NAME,
    user=config.DB_USER,
    host=config.DB_HOST,
    password=config.DB_PASSWORD,
    charset=config.DB_CHARSET,
)

sentry = Sentry()

# # 捕捉 celery 报错到 sentry
# sentry_client = SentryClient()
# register_signal(sentry_client)

CACHE_CONFIG = dict(
    CACHE_TYPE=config.CACHE_TYPE,
    CACHE_KEY_PREFIX=config.CACHE_KEY_PREFIX,
    CACHE_REDIS_URL=config.CACHE_REDIS_URL,
)
cache = PandoraCache(config=CACHE_CONFIG)
