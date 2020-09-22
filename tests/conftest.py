import os
import pytest
from poll import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///.test.db',
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()