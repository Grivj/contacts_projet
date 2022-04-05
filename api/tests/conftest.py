import json
from urllib.parse import urlencode


def client():
    from app import app

    app.app.config["TESTING"] = True
    return app.app.test_client()


def call_client(client, path, params):
    url = f"{path}?{urlencode(params)}"
    response = client.get(url)
    return json.loads(response.data.decode("utf-8"))
