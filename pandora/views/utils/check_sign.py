import hashlib

from pandora import config
from pandora.models.api_key import get_api_key_by_public_key
from pandora.core.exceptions import ApiKeyDoesNotExistError, ApiSignError, Error


def get_md5(d: dict, secret_key: str, salt: str=None) -> str:
    md5_str = ''
    for key, value in tuple(sorted(pair for pair in d.items())):
        md5_str += f'{key}{value}'
    md5_str += secret_key
    if salt:
        md5_str += salt
    md5_bytes = md5_str.encode('utf8')
    return hashlib.md5(md5_bytes).hexdigest()


def verify_md5(d, secret_key, salt=None):
    d = d.copy()
    try:
        api_sign = d.pop("api_sign")
        if get_md5(d, secret_key, salt=salt) == api_sign:
            return True
    except KeyError:
        pass
    return False


def check_sign(data: dict):
    if config.DEBUG:
        # DEBUG 模式不检查
        return
    # 检查 api_key
    public_key = data.get('api_key')
    if not public_key:
        raise ApiKeyDoesNotExistError(error=Error.api_key_does_not_exist)
    api_key = get_api_key_by_public_key(public_key)
    # verify_md5
    if not verify_md5(data, api_key.secret_key):
        raise ApiSignError(error=Error.api_sign_error)
