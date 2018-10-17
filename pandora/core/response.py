from flask import jsonify


def ok(content=None, status_code=200):
    msg = {
        'content': content or {},
    }
    return jsonify(msg), status_code


def error(errmsg='', error='invalid_request', errcode=0, status_code=400):
    msg = {
        'errcode': errcode,
        'error': error,
        'errmsg': errmsg,
    }
    return jsonify(msg), status_code
