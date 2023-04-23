from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
import re, urllib.parse



router = APIRouter()

def other_lines(id: int):
    convo_id = db.lines[id].convo_id
    num_lines = 0
    for line in db.lines.values():
        if line.convo_id == convo_id:
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
    * `num_other_lines`: The total number of lines in the conversation
    """


    if int(id) not in db.lines.keys():
        raise HTTPException(status_code=404, detail="line not found.")
    
    words = re.findall(r'\w+', db.lines[int(id)].line_text)
    num_words = len(words)

    sentences = re.split('[.?!]+', db.lines[int(id)].line_text)
    sentences = [s for s in sentences if s != '']
    num_sentences = len(sentences)

    line_info = {
        "num_words": num_words,
        "num_sentences": num_sentences,
        "num_other_lines": other_lines(int(id))
    }

    json = {
        "line_id": int(id),
        "character": db.characters[db.lines[int(id)].c_id].name,
        "age": db.characters[db.lines[int(id)].c_id].age or None,
        "movie": db.movies[db.lines[int(id)].movie_id].title,
        "line_info": line_info
    }

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

    return sorted_list[offset:limit + offset]


class line_source_options(str, Enum):
    character = "character"
    movie = "movie"

@router.get("/lines/from_source/{name}", tags=["lines"])
def list_lines_from_source(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    source: line_source_options = line_source_options.character,
):
    """
    This endpoint returns a list of lines. For each line it returns:
    * `line_id`: the internal id of the line. Can be used to query the
      `/lines/{line_id}` endpoint.
    * `text`: The text of the line.
    * `movie`: The movie the line is from.
    * `character`: The character that says the line.

    You can filter for lines that come from either a character or movie 
    by using the name query parameter and choosing the source. Input the exact name
    of the character or movie to return the lines.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    lines = []
    name_found = False

    if source == "character":
        
        for character, value in db.characters.items():
            if urllib.parse.unquote(name).lower() == value[0].lower():
                id = character
                name_found = True
                break

        if name_found == False:
            raise HTTPException(status_code=404, detail="character not found.")    
        
        for l, v in db.lines.items():
            if v[0] == id:
                line = {
                    "line_id": l,
                    "text": v[4],
                    "movie": db.movies[v[1]][0],
                    "character": db.characters[v[0]][0]
                }
                lines.append(line)

    if source == "movie":

        for movie, value in db.movies.items():
            if urllib.parse.unquote(name).lower() == value[0].lower():
                id = movie
                name_found = True
                break

        if name_found == False:
            raise HTTPException(status_code=404, detail="movie not found.")
            
        for l, v in db.lines.items():
            if v[1] == id:
                line = {
                    "line_id": l,
                    "text": v[4],
                    "movie": db.movies[id][0],
                    "character": db.characters[v[0]][0]
                }
                lines.append(line)

    return lines[offset : limit + offset]