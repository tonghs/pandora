from flask import g, request

from pandora.core.my_blueprint import MyBlueprint


def _factory(module_path, url_prefix, is_api=True):
    import_name = f'pandora.views.{module_path}'
    url_prefix = f'/api/v1{url_prefix}' if is_api else url_prefix
    print(import_name, url_prefix)
    bp = MyBlueprint(module_path, import_name, url_prefix=url_prefix)

    @bp.before_request
    def set_variables():
        if request.method == 'POST':
            request_data = request.get_json(force=True) or request.form.to_dict()
        else:
            request_data = request.values.to_dict()

        g.request_data = request_data

    return bp


index_blueprint = _factory('index', '', is_api=False)

all_blueprints = [
    index_blueprint
]
