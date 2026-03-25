from flask import render_template, current_app

from services.page_tools import get_header


def register_routes(app):
    from .wiki import wiki_bp
    from .calendar import calendar_bp
    from .contacts import contacts_bp
    from .tasks import tasks_bp
    app.register_blueprint(wiki_bp, url_prefix='/wiki')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(contacts_bp, url_prefix='/contacts')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    
    @app.route('/')
    def index():
        settings = current_app.config['SETTINGS']
        head = get_header(settings, 'About')
        return render_template('index.html', header = head, version=settings.version, logo = settings.name)
