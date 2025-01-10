from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass

bcrypt = Bcrypt()
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
loginManager = LoginManager()

def create_app(config_name="config"):
    app = Flask(__name__)
    app.config.from_object(config_name)

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    loginManager.init_app(app)

    loginManager.login_view = "users.login"
    loginManager.login_message = "Please log in access this page."
    loginManager.login_message_category = "warning"

    with app.app_context():
        from . import views

        from .posts import post_bp
        from .users import user_bp

        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp)
    return app
