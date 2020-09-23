class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'
    

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI: 'sqlite:///.test.db'

class ProductionConfig(Config):
    pass
    