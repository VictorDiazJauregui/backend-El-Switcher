from fastapi.testclient import TestClient
from fastapi import Request

from app.main import app
from app.errors.handlers import (
    NotFoundError,
    ForbiddenError,
    generic_exception_handler,
)

client = TestClient(app)


@app.get("/value_error")
async def trigger_value_error():
    raise ValueError("This is a value error")


@app.get("/generic_error")
async def trigger_generic_error(request: Request):
    try:
        raise Exception("This is a generic error")
    except Exception as e:
        return await generic_exception_handler(request, e)


@app.get("/not_found_error")
async def trigger_not_found_error():
    raise NotFoundError("This is a not found error")


@app.get("/forbidden_error")
async def trigger_forbidden_error():
    raise ForbiddenError("This is a forbidden error")


def test_value_error_handler():
    response = client.get("/value_error")
    assert response.status_code == 400
    assert response.json() == {"detail": "This is a value error"}


def test_generic_exception_handler():
    response = client.get("/generic_error")
    assert response.status_code == 500
    assert response.json() == {"detail": "This is a generic error"}


def test_not_found_error_handler():
    response = client.get("/not_found_error")
    assert response.status_code == 404
    assert response.json() == {"detail": "This is a not found error"}


def test_forbidden_error_handler():
    response = client.get("/forbidden_error")
    assert response.status_code == 403
    assert response.json() == {"detail": "This is a forbidden error"}
