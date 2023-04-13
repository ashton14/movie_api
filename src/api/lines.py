from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
import re

router = APIRouter()

def other_lines(id: str):
    num_lines = 0
    for line in db.lines.values():
        if line[2] == id:
            num_lines += 1
    
    return num_lines
        
            
@router.get("/lines/{id}", tags=["lines"])
def get_line(id: str):
    """
    This endpoint returns a single line by its identifier. For each line
    it returns:
    * `line_id`: the internal id of the line. Can be used to query the
      `/lines/{line_id}` endpoint.
    * `character`: The name of the character that said the line.
    * `age`: The age of the character.
    * `movie`: The movie the line is from.
    * `line_info`: A list of information about the line. The info is described below.

    The line info is represented by a dictionary with the following keys:
    * `num_words`: the number of words in the line.
    * `num_sentences`: the number of sentences in the line.
    * `num_other_lines`: The number of other lines in the same conversation
    """
    
    if id not in db.characters:
        raise HTTPException(status_code=404, detail="line not found.")
    
    delimiters = '[.,!?\\- ;:\\/\"\']+'
    words = re.split(delimiters, db.lines[id][4])
    words = [word for word in words if word != '']
    num_words = len(words)

    sentences = re.split('[.?!]+', db.lines[id][4])
    num_sentences = len(sentences)

    line_info = {
        "num_words": num_words,
        "num_sentences": num_sentences,
        "num_other_lines": other_lines(id)
    }

    json = {
        "line_id": int(id),
        "character": db.characters[db.lines[id][0]][0],
        "age": db.characters[db.lines[id][0]][3] if db.characters[db.lines[id][0]][3] != "" else None,
        "movie": db.movies[db.lines[id][1]][0],
        "line_info": line_info
    }

    
    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return json


class line_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    text = "text"


@router.get("/lines/", tags=["lines"])
def list_lines(
    subtext: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: line_sort_options = line_sort_options.character,
):
    """
    This endpoint returns a list of lines. For each line it returns:
    * `line_id`: the internal id of the line. Can be used to query the
      `/lines/{line_id}` endpoint.
    * `text`: The text of the line.
    * `movie`: The movie the line is from.
    * `character`: The character that says the line.

    You can filter for lines whose text contains a string by using the
    `subtext` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `text` - Sort by line text alphabetically
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    lines = []

    for line, value in db.lines.items():

        l = {
            "line_id": line,
            "text": value[4],
            "movie": db.movies[value[1]][0],
            "character": db.characters[value[0]][0]
        }
        lines.append(l)

    filtered_list = [x for x in lines if subtext.lower() in x["text"].lower() and x["text"] !=""]

    if sort == "character":
        sorted_list = sorted(filtered_list, key=lambda x: x["character"])   
    if sort == "movie":
        sorted_list = sorted(filtered_list, key=lambda x: x["movie"]) 
    if sort == "text":
        sorted_list = sorted(filtered_list, key=lambda x: x["text"])

    return sorted_list