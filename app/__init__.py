from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


def setup_swagger(app):
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Flask application for books managing"
        }
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)


def init_app():
    app = Flask(__name__)
    setup_swagger(app)
    from app.routes import books_bp
    app.register_blueprint(books_bp)
    return app
