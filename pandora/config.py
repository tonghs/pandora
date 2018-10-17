import os


# helpers
def _bool(v):
    if getattr(v, 'lower', None):
        return v.lower() in ('y', 'yes', 't', 'true', 'on', '1')
    return False


# general
DEBUG = _bool(os.getenv('DEBUG')) or os.getenv('ENV', '').lower().startswith('dev')
DOMAIN = os.getenv('DOMAIN', 'pandora.local')
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY', 'random-top-secret')

# database
DB_HOST = 'pandora-db-01'
DB_NAME = os.getenv('DB_NAME', 'pandora')
DB_PORT = 3306
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_CHARSET = 'utf8mb4'

# redis
REDIS_URL = "redis://pandora-redis-db:6379/0"

# cache
CACHE_TYPE = 'redis'
CACHE_KEY_PREFIX = 'pandora',
CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://pandora-redis-cache:6379/1')
