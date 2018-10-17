import datetime
import random

from peewee import CharField, DateTimeField

from pandora.models.base import BaseDAO
from ..dto.api_key import ApiKeyDTO


class ApiKeyDAO(BaseDAO):
    public_key = CharField(max_length=32, unique=True)
    secret_key = CharField(max_length=32)
    desc = CharField(max_length=128)
    app_name = CharField(max_length=32)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'api_key'


def get_api_key_by_public_key(public_key: str) -> ApiKeyDTO:
    apikey_dao = ApiKeyDAO.get(public_key=public_key)
    apikey_dto = ApiKeyDTO.from_dao(apikey_dao)
    return apikey_dto


def create_api_key(app_name: str, desc: str) -> ApiKeyDTO:
    dto = ApiKeyDTO(
        public_key="{:032x}".format(random.getrandbits(128)),
        secret_key="{:032x}".format(random.getrandbits(128)),
        app_name=app_name,
        desc=desc,
    )
    dao = ApiKeyDAO.create(**dto.dict_for_dao())
    return ApiKeyDTO.from_dao(dao)
