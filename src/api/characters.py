from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()

def topConversations(id: str): 
    
    top_convos = []

    for conversaton, value in db.conversations.items():

        dup = False

        if value[0] == id:
            convo = {
                "character_id": value[1],
                "character": db.characters[value[1]][0],
                "gender": db.characters[value[1]][2],
                "number_of_lines_together": num_lines_together(conversaton, conversaton[1])
            }
            if len(top_convos) == 0:
                top_convos.append(convo)
                continue

            for c in top_convos:
                if c["character_id"] == value[1]:
                    c["number_of_lines_together"] += conversaton["number_of_lines_together"]
                    dup = True
                    break
            if dup ==  False:
                top_convos.append(convo)

    return top_convos

def num_lines_together(convo: str, id: str):

    numLines = 0
    for value in db.lines.values():
        if value[2] == convo and value[0] == id:
            numLines += 1

    return numLines
        
            
@router.get("/characters/{id}", tags=["characters"])
def get_character(id: str):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """

    json = {
        "character_id": id,
        "character": db.characters[id][0],
        "movie": db.movies[db.characters[id][1]][0],
        "gender": db.characters[id][2],
        "top_conversations": topConversations(id)
    }

    
    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return json


class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: character_sort_options = character_sort_options.character,
):
    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    json = None
    return json
