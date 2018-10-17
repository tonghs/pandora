import fire

from pandora import config
from pandora.application import create_app
from pandora.core.apidoc import app_openapi_doc
from pandora.core.text import json_dumps
from pandora.models.utils.db import (
    create_database,
    create_tables,
    drop_database,
    drop_tables,
)


class Pandora:

    def run(self, port: int=9999):
        app = create_app(config)

        app.run(
            use_debugger=True,
            use_reloader=True,
            debug=True,
            host='0.0.0.0',
            port=port
        )

    def create_database(self):
        create_database()

    def drop_database(self):
        drop_database()

    def create_tables(self):
        create_tables()

    def drop_tables(self):
        drop_tables()

    def openapi_doc(self):
        app = create_app(config, init_db=False)
        return json_dumps(app_openapi_doc(app), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    fire.Fire(Pandora)
