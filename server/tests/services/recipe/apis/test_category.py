from flask.testing import FlaskClient


def test_category_get(client: FlaskClient):
    response = client.get("/api/v1/heathcheck")
    assert response.status_code == 200
