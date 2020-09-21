import os
import config
from flask import Flask
from flask_migrate import Migrate

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    if app.config['ENV'] == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from poll.models import db

    db.init_app(app)

    with app.app_context():
        db.create_all()
        migrate = Migrate(app, db)
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)
    
    # apply the blueprints to the app
    from poll import poll

    app.register_blueprint(poll.bp)

    return app