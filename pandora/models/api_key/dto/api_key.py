import datetime

from pydantic import BaseModel


class ApiKeyDTO(BaseModel):
    id: int = None      # type: ignore
    public_key: str = ''
    secret_key: str = ''
    desc: str = ...     # type: ignore
    app_name: str = ...     # type: ignore
    create_time: datetime.datetime = None       # type: ignore
    update_time: datetime.datetime = None       # type: ignore

    @classmethod
    def from_dao(cls, dao):
        return cls.parse_obj(dao.to_dict())

    def dict_for_dao(self) -> dict:
        return self.dict(exclude={'id', 'create_time', 'update_time'})
