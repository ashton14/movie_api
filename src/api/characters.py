from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()

def topConversations(id: str): 
    
    top_convos = []
    for conversation in db.conversations:
        if conversation["character1_id"] == id:
            c2id = conversation["character2_id"]
            for char in db.characters:
                if char["character_id"] == c2id:
                    c2name = char["name"]
                    c2gender = char["gender"]

        for conversation in db.conversations:
            if conversation["character1_id"] == id:
                if conversation["character2_id"] == c2id:
                    convo = {
                            "character_id": c2id,
                            "character": c2name,
                            "gender": c2gender,
                            "number_of_lines_together": 1
                            }
                    if convo not in top_convos:
                        top_convos.append(convo)
    
    return top_convos
        
            
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

    json = None

    for character in db.characters:
        if character["character_id"] == id:
            print("character found")
  
            json = {
               "character_id": character["character_id"],
                "character": character["name"],
                "movie": character["movie_id"],
                "gender": character["gender"],
                "top conversations": topConversations(id)
            }

            for movie in db.movies:
                if movie["movie_id"] == character["movie_id"]:
                    json["movie"] = movie["title"]

#            top_convos = []
#
 #           convo_id, numLines, c2id, c2name, c2gender = [], 0, 0, "", ""
  #            
   #         for conversation in db.conversations:
    #            if conversation["character1_id"] == id:
    #                c2id = conversation["character2_id"]
    #                break                    
    #                        
    #        for conversation in db.conversations:
    #            if conversation["character1_id"] == id:
    #                if conversation["character2_id"] == c2id:
    #                    if conversation["conversation_id"] not in convo_id:
    #                        convo_id.append(conversation["conversation_id"])
    #                else:
    #                    for char in db.characters:
    #                        if char["character_id"] == c2id:
    #                            c2name = char["name"]
    #                            c2gender = char["gender"]
    #                                    
    #                    convo = {
    #                        "character_id": c2id,
    #                        "character": c2name,
    #                        "gender": c2gender,
    #                        "number_of_lines_together": numLines
    #                    }
    #                    top_convos.append(convo)
    #                    numLines = 1
    #                    c2id = conversation["character2_id"]
    #                    continue    
    #
    #            else:
    #                if len(convo_id) > 0: 
    #                    for c in convo_id:
    #                        for line in db.lines:
    #                            if line["conversation_id"] == c:
    #                                if line["character_id"] == c2id:
    #                                    numLines += 1
    #                        
    #                        for char in db.characters:
    #                            if char["character_id"] == c2id:
    #                                c2name = char["name"]
    #                                c2gender = char["gender"]
#
#                            convo = {
#                                "character_id": c2id,
#                                "character": c2name,
#                                "gender": c2gender,
#                                "number_of_lines_together": numLines
#                            }
#                            
#                            top_convos.append(convo)
#                        break
#                                

            #json["top conversations"] = top_convos
            

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
