import inspect
from functools import wraps

from flask import Blueprint, g
from pydantic import BaseModel, ValidationError

from pandora import config
from pandora.core.exceptions import PandoraBaseException, Error
from pandora.core.response import error, ok


class MyBlueprint(Blueprint):

    def rpc_route(self, rule, methods=('POST',), **options):
        orig_decorator = self.route(rule, methods=methods, **options)

        def decorator(f):
            sig = inspect.signature(f, follow_wrapped=True)
            req_type = list(sig.parameters.values())[0].annotation if sig.parameters else None

            @wraps(f)
            def _(*args, **kwargs):
                try:
                    if req_type and issubclass(req_type, BaseModel):
                        j = req_type.parse_obj(g.request_data)
                        args = args[1:]
                        func_ret = f(j, *args, **kwargs)
                        return ok(func_ret.dict() if func_ret else None)
                    else:
                        func_ret = f(*args, **kwargs)
                        return ok(func_ret.dict() if func_ret else None)
                except ValidationError as e:
                    error_code, error_msg = Error.invalid_args
                    if config.DEBUG:
                        error_msg = error_msg + ': ' + str(e)
                    return error(errmsg=error_msg, error='invalid_request', errcode=error_code, status_code=400)
                except PandoraBaseException as e:
                    error_msg = e.error_msg
                    if config.DEBUG:
                        error_msg = error_msg + ': ' + str(type(e)) + ': ' + str(e)
                    return error(errmsg=error_msg, errcode=e.error_code)

            _.is_custom = True
            return orig_decorator(_)

        return decorator

    def rpc(self, f):
        return self.rpc_route(rule=f'/{f.__name__}')(f)
