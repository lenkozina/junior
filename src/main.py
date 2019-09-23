"""Модуль запуска сервера."""

from flask import Flask
from flask_admin.contrib.sqla import ModelView

from src import user
from src.extensions import admin, bcrypt, db, migrate, sess
from src.settings import DevelopConfig
from src.user import User
from src.views import index_bp


def create_app(config=DevelopConfig):
    """App factory."""
    app = Flask(
        __name__.split('.')[0],
    )
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_adminpanel(app)
    register_sessions(app)
    return app


def register_extensions(app):
    """Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)


def register_adminpanel(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    admin.add_view(ModelView(User, db.session))


def register_sessions(app):
    # Session storage type.
    app.config['SESSION_TYPE'] = 'filesystem'

    # Max sess file before start deleting.
    app.config['SESSION_FILE_THRESHOLD'] = 100
    sess.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user.views.bp)
    app.register_blueprint(index_bp)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
        }

    app.shell_context_processor(shell_context)
