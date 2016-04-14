import os


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_NAME = "blog"

    DEBUG = True
    SECRET_KEY = "$2a$12$LdKsgm9HGNC6LzKVzJ48ju"

    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/codeventuri"
    SQLALCHEMY_DATABASE_URI = "postgresql:///codeventuri"


    # Load a database URL from configuration if it exists
    if os.environ.get("DATABASE_URL"):
        url = os.environ.get("DATABASE_URL").replace(
            "postgres://", "postgresql+psycopg2://")

        if "postgresql" in url and "?" not in url:
            # Force SSL (useful for remotely connecting to Heroku Postgres)
            url = url + "?sslmode=require"

        SQLALCHEMY_DATABASE_URI = url

    if os.name == "nt":
        LESS_BIN = "lessc.cmd"
        COFFEE_BIN = "coffee.cmd"

    # Debug
    ASSETS_MINIFY = False
    ASSETS_USE_CDN = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'codeventuri.blog@gmail.com'
    MAIL_PASSWORD = 'codeventuri123'

    DEFAULT_MAIL_SENDER = ("Codeventuri-Blog", "codeventuri.blog@gmail.com")

    # Flask-Security Flags
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True

    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_PASSWORD_SALT = "$2a$12$sSoMBQ9V4hxNba5E0Xl3Fe"
    SECURITY_CONFIRM_SALT = "$2a$12$QyCM19UPUNLMq8n225V7qu"
    SECURITY_RESET_SALT = "$2a$12$GrrU0tYteKw45b5VfON5p."
    SECURITY_REMEMBER_SALT = "$2a$12$unlKF.sL4gnm4icbk0tvVe"

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True

    ASSETS_MINIFY = True
    ASSETS_USE_CDN = True
