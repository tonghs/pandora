from peewee import DoesNotExist

from pandora.core.exceptions import ApiKeyDoesNotExistError, Error
from .dto.api_key import ApiKeyDTO
from .dao import api_key as api_key_api


def get_api_key_by_public_key(public_key: str) -> ApiKeyDTO:
    try:
        return api_key_api.get_api_key_by_public_key(public_key)
    except DoesNotExist:
        raise ApiKeyDoesNotExistError(error=Error.api_key_does_not_exist)
