from flask import g, request

from pandora.core.my_blueprint import MyBlueprint
from pandora.views.utils.check_sign import check_sign


def _factory(module_path, url_prefix):
    import_name = f'pandora.views.{module_path}'
    bp = MyBlueprint(module_path, import_name, url_prefix=f'/api/v1{url_prefix}')

    @bp.before_request
    def set_variables():
        if request.method == 'POST':
            request_data = request.get_json(force=True) or request.form.to_dict()
        else:
            request_data = request.values.to_dict()

        check_sign(request_data)

        g.request_data = request_data

    return bp


all_blueprints = [
]
