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


def test_add_conversation1():
    
    convo = {
        "character_1_id": 631,
        "character_2_id": 641,
        "lines": [
            {
            "character_id": 631,
            "line_text": "My name is" + db.characters[631].name
            },
            {
            "character_id": 641,
            "line_text": "My name is" + db.characters[641].name
            }
        ]
}
    response = client.post("/movies/40/conversations/", json=convo)
    assert response.status_code == 200


    assert db.char_lines[len(db.char_lines)-1]["character_id"] == convo["character_2_id"]