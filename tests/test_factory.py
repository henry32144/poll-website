from poll import create_app


def test_config():
    assert not create_app('production').testing
    assert not create_app('development').testing
    assert create_app('testing').testing


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200