import datetime
import random
import string
from typing import Any

import ujson


def random_str(length=10):
    all_str = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.sample(all_str, length))


def is_chinese_char(c):
    """判断一个 unicode 字符是否是汉字"""
    return '\u4e00' <= c <= '\u9fa5'


def is_number_char(c):
    """判断一个 unicode 字符是否是数字"""
    return '\u0030' <= c <= '\u0039'


def is_alphabet_char(c):
    """判断一个 unicode 字符是否是英文字母"""
    return '\u0041' <= c <= '\u005a' or '\u0061' <= c <= '\u007a'


def is_legal_char_for_user_name(c):
    """可用于用户名的字符"""
    return is_chinese_char(c) or is_number_char(c) or is_alphabet_char(c) or c in ('-', '_')


def has_illegal_txt_for_user_name(s):
    '''是否包含不可用于用户名的字符'''
    for c in s:
        if not is_legal_char_for_user_name(c):
            return True
    return False


def filter_illegal_txt_for_user_name(s):
    '''过滤掉不可用于用户名的字符'''
    cs = [c for c in s if is_legal_char_for_user_name(c)]
    return ''.join(cs)


def humanize_time(date: Any) -> str:
    """ https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python """

    now = datetime.datetime.now()
    if type(date) is int:
        diff = now - datetime.datetime.fromtimestamp(date)

    elif isinstance(date, datetime.datetime):
        diff = now - date

    else:
        return date

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return date

    if day_diff == 0 or day_diff == -1:
        if second_diff < 10:
            return "刚刚"
        if second_diff < 60:
            return f"{int(second_diff)}秒前"
        if second_diff < 120:
            return "一分钟前"
        if second_diff < 3600:
            return f"{int(second_diff / 60)}分钟前"
        if second_diff < 7200:
            return "一小时前"
        if second_diff < 86400:
            return f"{int(second_diff / 3600)}小时前"

    if day_diff == 1:
        return "昨天"
    if day_diff < 7:
        return f"{day_diff}天前"
    if day_diff < 31:
        return f"{int(day_diff / 7)}个星期前"
    if day_diff < 365:
        return f"{int(day_diff / 30)}个月前"
    return f"{int(day_diff / 365)}年前"


def json_dumps(data: Any, *args, **kw) -> str:
    return ujson.dumps(data, *args, **kw)


def json_loads(data: str, *args, **kw) -> Any:
    return ujson.loads(data, *args, **kw)


