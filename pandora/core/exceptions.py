from enum import Enum


class Error(tuple, Enum):
    """ 用来最终交给客户端指明需要特殊处理的情况的错误 """
    common = (1000, '请求错误')
    invalid_args = (1001, '请求参数错误')
    api_key_does_not_exist = (1102, 'api_key 不存在')
    api_sign_error = (1103, 'API 签名错误')


class PandoraBaseException(Exception):
    """
    内部处理过程中的异常
    """

    def __init__(self, error_msg='', error=Error.common):
        self.error_code = error[0]
        self.error_msg = error_msg or error[1]


class ApiKeyDoesNotExistError(PandoraBaseException):
    pass


class ApiSignError(PandoraBaseException):
    pass


class ConcurrentWriteError(PandoraBaseException):
    pass
