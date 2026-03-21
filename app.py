import os
import sys
from flask import Flask
from common.rails_context import RailsContext
from services.config_tools import read_config, ConfigTools


def create_app():
	app = Flask(__name__)
	context = RailsContext()
	settings = ConfigTools()
	settings.load_config(context, 'config.json')
	if context.hasError():
		print(f"Cannot start server: {context.error}")
		sys.exit(1)
	app.config['SETTINGS'] = settings

	from routes import register_routes
	register_routes(app)
	return app

if __name__ == '__main__':
	app = create_app()
	app.run(debug=True, port=5005)

