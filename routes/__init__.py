from flask import render_template

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
        return render_template('index.html')
