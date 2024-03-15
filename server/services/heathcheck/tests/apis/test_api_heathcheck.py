import json
from flask.testing import FlaskClient


def test_heathcheck(client: FlaskClient):
    # given

    # when
    response = client.get("/api/v1/heathcheck")

    status_code = response.status_code
    res_data = json.loads(response.data.decode("utf-8"))

    # then
    assert status_code == 200
    assert res_data == {"heathcheck": "ok"}
