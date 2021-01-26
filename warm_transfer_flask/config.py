import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
    TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY', None)
    TWILIO_API_SECRET = os.environ.get('TWILIO_API_SECRET', None)
    TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
    TWIML_APPLICATION_SID = os.environ.get('TWIML_APPLICATION_SID', None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')


class TestConfig(DefaultConfig):
    TWILIO_ACCOUNT_SID = 'ACxxx'
    TWILIO_API_KEY = 'SKxxx'
    TWILIO_API_SECRET = 'xxxxx'
    TWILIO_NUMBER = '+55'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True


config_classes = {
    'testing': TestConfig,
    'development': DevelopmentConfig,
    'production': DefaultConfig,
}
