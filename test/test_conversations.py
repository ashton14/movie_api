from fastapi.testclient import TestClient

from src.api.server import app

from src import database as db

import json

client = TestClient(app)


def test_add_conversation():

    convo = {
        "character_1_id": 0,
        "character_2_id": 3,
        "lines": [
            {
            "character_id": 0,
            "line_text": "This is the first new line!!!"
            },
            {
            "character_id": 3,
            "line_text": "This is the second new line!!!"
            }
        ]
}
    response = client.post("/movies/0/conversations/", json=convo)
    assert response.status_code == 200


    assert db.convos[len(db.convos)-1]["character1_id"] == convo["character_1_id"]


#def test_add_conversation1():
    