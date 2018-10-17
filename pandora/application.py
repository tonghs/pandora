from importlib import import_module

from flask import Flask

from pandora.blueprints import all_blueprints
from pandora.extensions import CustomJSONEncoder, cache, sentry
from pandora.models.utils.db import create_tables


def create_app(config, init_db=True):
    if init_db:
        create_tables()

    app = Flask(__name__, template_folder='templates')
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config)

    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    sentry.init_app(app)
    cache.init_app(app)

    return app
