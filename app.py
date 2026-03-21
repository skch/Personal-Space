import os
import sys
from flask import Flask
from common.rails_context import RailsContext
from services.config_tools import read_config


def create_app():
	app = Flask(__name__)

	context = RailsContext()
	config_path = os.path.join(app.root_path, 'config.json')
	config_data = read_config(context, config_path)
	if context.hasError():
		print(f"Cannot start server: {context.error}")
		sys.exit(1)
	app.config.update(config_data)

	from routes import register_routes
	register_routes(app)
	return app

if __name__ == '__main__':
	app = create_app()
	app.run(debug=True, port=5005)

