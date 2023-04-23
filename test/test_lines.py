from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)
"""

def test_get_line():
    response = client.get("/lines/486263")
    assert response.status_code == 200

    with open("test/lines/486263.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_line1():
    response = client.get("/lines/6789")
    assert response.status_code == 200

    with open("test/lines/6789.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_lines():
    response = client.get("/lines/?subtext=disaster&sort=movie")
    assert response.status_code == 200

    with open("test/lines/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines1():
    response = client.get(
        "/lines/?subtext=complicated&limit=5&offset=0&sort=text"
    )
    assert response.status_code == 200

    with open(
        "test/lines/subtext=complicated&limit=5&offset=0&sort=text.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)


def test_line_by_source():
    response = client.get(
        "/lines/from_source/veronica?limit=5&offset=0&source=character"
    )
    assert response.status_code == 200

    with open(
        "test/lines/name=veronica&limit=5&source=character.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)


def test_line_by_source1():
    response = client.get(
        "/lines/from_source/the exorcist?limit=4&source=movie"
    )
    assert response.status_code == 200

    with open(
        "test/lines/name=the exorcist&limit=4&source=movie.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)


def test_404():
    response = client.get("/lines/400")
    assert response.status_code == 404
"""