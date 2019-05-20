import pytest
import os
from server import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_unauthorized_upload_no_token(client):
    data = {}
    data["file"] = open("./test/data.xlsx", "rb")
    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 401


def test_unauthorized_upload_bad_token(client):
    data = {}
    data["file"] = open("./test/data.xlsx", "rb")
    response = client.post(
        "/",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": "Token {}bad".format(
                os.getenv("API_VERIFICATION_TOKEN", "")
            )
        },
    )
    assert response.status_code == 403
