from functools import wraps


def setup_dto_stats(dto, setup_func=None):
    """ 给 dto 设置一些在不同 Model 上的属性

    :param dto: dto 类型 eg. ShowDTO
    :param setup_func: 设置 dto 属性的方法，签名为 setup_func(List[dto]) -> List[dto]
    """
    def deco(func):
        @wraps(func)
        def inner(*args, **kw):
            ret = func(*args, **kw)
            if isinstance(ret, dto):
                if not setup_func:
                    return ret
                setup_func([ret])
                return ret

            if isinstance(ret, dict):
                ret_tmp = list(filter(None, ret.values()))
            elif isinstance(ret, list):
                ret_tmp = list(filter(None, ret))
            else:
                return ret

            if list(filter(lambda x: not isinstance(x, dto), ret_tmp)):
                return ret

            setup_func(ret_tmp)

            return ret
        return inner
    return deco
