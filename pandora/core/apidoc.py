import inspect
import re
from enum import EnumMeta
from typing import Union

from pydantic import BaseModel
from pydantic.fields import Shape

from pandora import config


def is_field_openapi_model(field):
    """
    检查是不是可以转换成 openapi model 的类型
    """
    if issubclass(field.type_, BaseModel):
        return True
    elif issubclass(type(field.type_), EnumMeta):
        return True
    return False


def is_field_union_model(field):
    """
    检查是不是 union model，需要特殊处理
    """
    return getattr(field.type_, '__origin__', None) is Union


def is_model_base_model(model):
    if issubclass(model, BaseModel):
        return True


def is_model_enum(model):
    return issubclass(type(model), EnumMeta)


def traverse_field_to_get_models(field):
    models = set()
    if is_field_openapi_model(field):
        model = field.type_
        models.add(model)
        models.update(traverse_model_to_get_models(model))
    elif is_field_union_model(field):
        for sub_field in field.sub_fields:
            models.update(traverse_field_to_get_models(sub_field))
    return models


def traverse_model_to_get_models(model):
    models = set()
    if not is_model_base_model(model):
        return models

    for _, field in model.__fields__.items():
        models.update(traverse_field_to_get_models(field))
    return models


def traverse_view_funcs_to_get_models(app):
    models = set()
    for rule in app.url_map.iter_rules():
        # 过滤旧 view
        if not str(rule).startswith('/api/v1'):
            continue
        view_func = app.view_functions[rule.endpoint]
        sig = inspect.signature(view_func, follow_wrapped=True)
        if sig.parameters.items():
            req_model = list(sig.parameters.items())[0][1].annotation
        else:
            req_model = None

        resp_model = sig.return_annotation
        if req_model and issubclass(req_model, BaseModel):
            models.add(req_model)
            models.update(traverse_model_to_get_models(req_model))

        if resp_model and issubclass(resp_model, BaseModel):
            models.add(resp_model)
            models.update(traverse_model_to_get_models(resp_model))
    return models


def trans_python_type_to_openapi_type(type_: str) -> str:
    if type_ == 'int':
        return 'integer'
    elif type_ == 'str':
        return 'string'
    elif type_ == 'bool':
        return 'boolean'
    elif type_ == 'datetime':
        return 'string'
    elif type_ in ('float', 'double'):
        return 'number'
    return 'string'
    # TODO:
    # array and object
    # raise TypeError(f'unsupported {type_}')


def trans_field_to_spec(field):
    if is_field_openapi_model(field):
        model = field.type_
        spec = {
            '$ref': f'#/components/schemas/{model.__name__}'
        }
    elif is_field_union_model(field):
        spec = {
            'oneOf': [{'$ref': f'#/components/schemas/{sub_field.type_.__name__}'} for sub_field in field.sub_fields],
        }
    else:
        spec = {
            'type': trans_python_type_to_openapi_type(field.type_.__name__),
            'description': field.type_.__name__ if field.type_.__name__ in ('datetime',) else '',
        }
    # 处理 list 类型
    if field.shape == Shape.LIST:
        spec = {
            'type': 'array',
            'items': spec
        }
    return spec


def trans_model_to_spec(model):
    if is_model_base_model(model):
        properties = {}
        spec = {
            'description': model.__doc__ or '',
            'properties': properties,
        }
        for name, field in model.__fields__.items():
            properties[name] = trans_field_to_spec(field)
    elif is_model_enum(model):
        enum_values = []
        k_v_items = []
        for k, v in model.__members__.items():
            enum_values.append(int(v))
            k_v_items.append(f'{k}({int(v)})')
        spec = {
            'type': 'integer',
            'description': '\n'.join(k_v_items),
            'enum': enum_values,
        }
    else:
        return
        # raise ValueError(f'not supported model {model.__name__}')
    return spec


def trans_model_to_get_parameters_spec(model):
    """ 将 view_func 的参数转成请求参数

    :param model: `<Parameter>`
    :return: param list
    """
    parameters = []

    # url 里带 **_id
    # FIXME: URL 带其他（非 int）类型时需要再看看
    if issubclass(model.annotation, int):
        parameters.append({
            'in': 'path',
            'name': model.name,
            'description': model.name,
            'schema': {
                'type': "integer",
            }
        })
        return parameters

    if not isinstance(model.annotation, BaseModel):
        return parameters

    for name, field in model.__fields__.items():
        spec = {
            'in': 'query',
            'name': name,
            'description': field.type_.__name__ if field.type_.__name__ in ('datetime',) else '',
            'schema': {
                'type': trans_python_type_to_openapi_type(field.type_.__name__)
            }
        }
        parameters.append(spec)
    return parameters


def trans_view_to_spec(rule, view_func, tag='default'):
    sig = inspect.signature(view_func, follow_wrapped=True)
    req_models = list(sig.parameters.values())

    method = list(rule.methods & {'GET', 'POST'})[0]
    request_content = {"application/json": {"schema": {}}}
    parameters = []
    return_schema = sig.return_annotation.__name__ if sig.return_annotation else 'NoneResp'

    schema = {
        '$ref': f"#/components/schemas/{return_schema}"
    }

    responses = {
        '200': {
            "description": "请求成功",
            'content': {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "content": schema,
                            "status": {
                                "type": "string",
                                "example": "ok",
                            }
                        },
                    }
                }
            },
        },
        '400': {
            "description": "请求出错",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ErrorResp"
                    }
                }
            },
        }
    }
    view_doc = (view_func.__doc__ or '').strip()
    view_doc_lines = view_doc.splitlines() or ['']
    summary = view_doc_lines[0]
    description = '\n'.join(view_doc_lines[1:])
    if method == 'POST':
        spec = {
            'post': {
                'summary': summary,
                'description': description,
                'requestBody': {
                    'content': request_content,
                },
                'responses': responses,
                'tags': [tag],
            }
        }
    elif method == 'GET':
        spec = {
            'get': {
                'summary': summary,
                'description': description,
                'parameters': parameters,
                'responses': responses,
                'tags': [tag],
            }
        }
    else:
        raise ValueError('unsupported method')

    if req_models and issubclass(req_models[0].annotation, BaseModel):
        _model = req_models[0].annotation
        post_schema = {
            "$ref": f"#/components/schemas/{_model.__name__}"
        }
    else:
        post_schema = {}

    if not req_models:
        return spec

    if method == 'POST':
        request_content["application/json"] = {
            "schema": post_schema
        }
    elif method == 'GET':
        for req_model in req_models:
            parameters.extend(trans_model_to_get_parameters_spec(req_model))

    return spec


def trans_path_param_url(url_path: str) -> str:
    """ 将 URL 中的 <int:k_id> 转换成 swagger 的 {k_id} """
    pattern = re.compile('(?P<kid><int:(?P<value>\w+)>)')

    def trans_param(matched):
        
        return "{%s}" % matched.group("value")
        

    return re.sub(pattern, trans_param, url_path)


def get_interface_tag(url_endpoint, app):
    for endpoint, _ in app.blueprints.items():
        if url_endpoint.startswith(endpoint):
            return endpoint

    return 'default'


def app_openapi_doc(app):
    component_schemas = {}
    paths = {}
    doc = {
        'openapi': '3.0.1',
        'info': {
            'version': '1.0.0',
            'title': f'{app.name} API'
        },
        'servers': [
            {
                'url': f'https://{config.DOMAIN}'
            }
        ],
        'paths': paths,
        'components': {
            'schemas': component_schemas
        }
    }

    # collect models
    models = traverse_view_funcs_to_get_models(app)

    # trans models to component schemas
    for model in models:
        spec = trans_model_to_spec(model)
        component_schemas[model.__name__] = spec

    component_schemas['ErrorResp'] = {
        'description': 'error',
        'properties': {
            'errcode': {
                'type': 'integer'
            },
            'error': {
                'type': 'string'
            },
            'errmsg': {
                'type': 'string'
            },
        },
    }

    # trans views to paths
    for rule in app.url_map.iter_rules():
        rule_tag = get_interface_tag(rule.endpoint, app)
        # 过滤旧 view
        if not str(rule).startswith('/api/v1'):
            continue
        view_func = app.view_functions[rule.endpoint]
        if getattr(view_func, 'is_custom', False):
            # 创建 view_doc
            spec = trans_view_to_spec(rule, view_func, tag=rule_tag)
            if spec:
                paths[trans_path_param_url(str(rule.rule))] = spec
    return doc
