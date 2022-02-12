from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_jwt_extended import ( JWTManager,
                                 jwt_required,
                                  create_access_token,
                                  get_jwt_identity
                                )


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .posts import posts_bp
        from .accounts import accounts_bp
        from .story import story_bp
        from .jobs import jobs_bp
        #from .story import story_bp

        # Register Blueprints
        app.register_blueprint(accounts.accounts_bp)
        app.register_blueprint(posts.posts_bp)
        app.register_blueprint(jobs.jobs_bp)
        app.register_blueprint(story.story_bp)



        return app
