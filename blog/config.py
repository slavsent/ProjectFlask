import os
from dotenv import load_dotenv
from blog.enums import EnvType

load_dotenv()

ENV = os.getenv('FLASK_ENV', default=EnvType.production)
DEBUG = ENV == EnvType.development

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True

FLASK_ADMIN_SWATCH = 'cosmo'

OPENAPI_URL_PREFIX = '/api/docs'
OPENAPI_SWAGGER_UI_PATH = '/'
OPENAPI_SWAGGER_UI_VERSION = '4.18.1'
