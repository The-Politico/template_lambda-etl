import pytest
import os
from server import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_bad_data(client):
    data = {}
    data["file"] = open("./test/bad_data.xlsx", "rb")
    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": "Token {}".format(
                os.getenv("API_VERIFICATION_TOKEN", "")
            )
        },
    )
    assert response.status_code == 500


def test_data_upload(client):
    data = {}
    data["file"] = open("./test/data.xlsx", "rb")
    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": "Token {}".format(
                os.getenv("API_VERIFICATION_TOKEN", "")
            )
        },
    )
    assert response.status_code == 200
