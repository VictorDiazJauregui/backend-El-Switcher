import pytest
from fastapi.testclient import TestClient
from fastapi import Request
from app.main import app
from app.errors.handlers import generic_exception_handler

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

@app.get("/validation_error")
async def trigger_validation_error(param: int):
    return {"param": param}

def test_value_error_handler():
    response = client.get("/value_error")
    assert response.status_code == 400
    assert response.json() == {"message": "This is a value error"}

def test_generic_exception_handler():
    response = client.get("/generic_error")
    assert response.status_code == 500
    assert response.json() == {"message": "An internal server error occurred."}

def test_validation_exception_handler():
    response = client.get("/validation_error?param=not_an_int")
    assert response.status_code == 422
    assert "message" in response.json()
    assert response.json()["message"][0]["type"] == "int_parsing"