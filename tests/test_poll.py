import pytest
from poll.models import db
from poll.models import Poll, Answer, Vote

def test_create_poll(client, app):
    # Delete first
    with app.app_context():
        Poll.query.filter_by(question='What do you want').delete()

    assert client.get('/').status_code == 200
    response = client.post(
        '/poll', data={'questionTitle': 'What do you want',
            'answer': ['money', 'gold', 'power'],
            'maxSelectionLimit': 1}
    )
    assert '/share' in response.headers['Location']

    with app.app_context():
        assert Poll.query.filter_by(question='What do you want').first() is not None

@pytest.mark.parametrize(('questionTitle', 'answer', 'maxSelectionLimit', 'status_code'), (
    ('', '', '', 422),
    (None, None, None, 422),
    ('a', '', 'a', 422),
    ('', ['test'], '1', 422),
    ('', [None, None], '1', 422),
))
def test_register_validate_input(client, questionTitle, answer, maxSelectionLimit, status_code):
    response = client.post(
        '/poll',
        data={'questionTitle': questionTitle,
         'answer': answer,
         'maxSelectionLimit': maxSelectionLimit}
    )
    assert response.status_code == status_code