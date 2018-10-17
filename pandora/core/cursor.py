import base64
from typing import Any, List

from pydantic import BaseModel


def get_base_id_and_max_size(cursor: Any = None, size: Any = None):
    if isinstance(cursor, str):
        cursor = int(base64.urlsafe_b64decode(
            cursor.strip())) if cursor else None
    if isinstance(size, str):
        size = int(size.strip()) if size else None
    return cursor, size


def encode_cursor(id: int):
    if not id:
        return ''
    return base64.urlsafe_b64encode(str(id).encode('utf-8'))


def gen_next_cursor(objs: List[Any], size: int):
    if len(objs) == size:
        next_cursor = encode_cursor(objs[-1].id)
    else:
        next_cursor = ''

    return next_cursor


class CursorReq(BaseModel):
    cursor: str = ''
    size: int = 20

    @property
    def cursor_int(self):
        return get_base_id_and_max_size(self.cursor)[0] or 0


CursorDTO = CursorReq


class CursorResp(BaseModel):
    prev_cursor: str = ''
    next_cursor: str = ''
    has_next: bool = False
    has_prev: bool = False

    @classmethod
    def from_objs_and_cursor(cls, objs: List[Any], cursor: CursorDTO):
        next_cursor = gen_next_cursor(objs, cursor.size)
        return CursorResp(
            prev_cursor=cursor.cursor,
            next_cursor=next_cursor,
            has_next=bool(next_cursor),
            has_prev=bool(cursor.cursor),
        )

    @classmethod
    def from_cursor(cls, prev_cursor='', next_cursor=''):
        return CursorResp(
            prev_cursor=prev_cursor,
            next_cursor=next_cursor,
            has_next=bool(next_cursor),
            has_prev=bool(prev_cursor),
        )
