from backend_app import create_app
import pytest

# @pytest.fixture
# def app():
#     app = create_app()
#     return app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

