import os
import tempfile

import pytest

import views



@pytest.fixture
def client():
    db_fd, views.app.config['DATABASE'] = tempfile.mkstemp()
    views.app.config['TESTING'] = True
    client = views.app.test_client()

    with views.app.app_context():
        views.init_db()

    yield client

    os.close(db_fd)
    os.unlink(views.app.config['DATABASE'])


