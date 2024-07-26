import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    )

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
