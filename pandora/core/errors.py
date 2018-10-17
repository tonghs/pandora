from werkzeug._compat import text_type
from werkzeug.exceptions import HTTPException

from pandora.core.text import json_dumps


class APIException(HTTPException):
    code = 400
    error = 'bad_request'

    def __init__(self, errmsg='', errcode=0, description=None, response=None):
        self.errmsg = errmsg
        self.errcode = errcode
        super(APIException, self).__init__(description, response)

    def get_body(self, environ=None):
        return text_type(json_dumps({
            'errcode': self.errcode,
            'error': self.error,
            'errmsg': self.errmsg,
        }))

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class FormError(APIException):
    code = 400
    errcode = 1001
    error = 'invalid_form'


class NotAuth(APIException):
    code = 401
    error = 'require_login'
    description = 'Authorization is required'


class NotFound(APIException):
    code = 404
    error = 'not_found'


class Denied(APIException):
    code = 403
    error = 'permission_denied'


class InvalidAccount(APIException):
    code = 403
    error = 'invalid_account'
    description = 'Your accounts is invalid'


class InvalidClient(APIException):
    code = 418
    error = 'your client is a teapot'


class SessionExpired(APIException):
    code = 463
    error = 'session expired'
