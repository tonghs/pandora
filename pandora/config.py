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
DB_USER = os.getenv('DB_USER', 'xcf')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'xcf@xiachufang.com')
DB_CHARSET = 'utf8mb4'
