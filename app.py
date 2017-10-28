from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware

import config
from views import home, json_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(home.bp)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/api': json_api})

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.debug, threaded=True)
