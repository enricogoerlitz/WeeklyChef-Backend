from flask.testing import FlaskClient


def test_heathcheck(client: FlaskClient):
    response = client.get("/api/v1/heathcheck")
    assert response.status_code == 200
