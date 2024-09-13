from .backend_app import create_app
import pytest


@pytest.fixture
def client():
    app = create_app()
    with app.app_context():
        with app.test_client() as client:
            yield client
