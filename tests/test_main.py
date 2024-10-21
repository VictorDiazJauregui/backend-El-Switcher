from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to The Switcher API"}


@patch("app.main.Base.metadata.create_all")
def test_lifespan(mock_create_all):
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        mock_create_all.assert_called_once()
