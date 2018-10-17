from flask_mako import render_template
from pandora.blueprints import index_blueprint as bp


@bp.route('/')
def index():
    return render_template('index.html')
