from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
import re, urllib.parse
import sqlalchemy
from sqlalchemy import func



router = APIRouter()

def other_lines(id: int):
    convo_id = db.lines[id].conv_id
    num_lines = 0
    for line in db.lines.values():
        if line.conv_id == convo_id:
            num_lines += 1
    
    return num_lines
        
            
@router.get("/lines/{id}", tags=["lines"])
def get_line(id: str):
    """
    This endpoint returns a single line by its identifier. For the line
    it returns:
    * `line_id`: the internal id of the line. Can be used to query the
      `/lines/{line_id}` endpoint.
    * `text`: The text of the line.
    * `character`: The name of the character that said the line.
    * `age`: The age of the character.
    * `movie`: The movie the line is from.
    * `line_info`: A list of information about the line. The info is described below.

    The line info is represented by a dictionary with the following keys:
    * `num_words`: the number of words in the line.
    * `num_sentences`: the number of sentences in the line.
    * `num_total_lines`: The total number of lines in the conversation
    """

    line_query = sqlalchemy.select(
        db.lines.c.line_id,
        db.lines.c.line_text,
        db.lines.c.conversation_id,
        db.characters.c.name,
        db.characters.c.age,
        db.movies.c.title,
    ).select_from(
        db.lines.join(db.characters, db.lines.c.character_id == db.characters.c.character_id)
        .join(db.movies, db.movies.c.movie_id == db.characters.c.movie_id)
        .join(db.conversations, db.conversations.c.conversation_id == db.lines.c.conversation_id)
    ).where(db.lines.c.line_id == id)
    

    line = db.engine.connect().execute(line_query).fetchone()

    if line is None:
        raise HTTPException(422, "Line not found.")

    convo_id = line.conversation_id

    num_total_lines_query = sqlalchemy.select(
        sqlalchemy.func.count().label("num_total_lines")
    ).select_from(
        db.lines.join(db.conversations, db.lines.c.conversation_id == db.conversations.c.conversation_id)
    ).where(
        db.conversations.c.conversation_id == convo_id
    )

    with db.engine.connect() as conn:
        num_total_lines = conn.execute(num_total_lines_query).scalar()

    sentences = re.split('[.?!]+', line.line_text)
    num_sentences = len([s for s in sentences if s != ''])

    response = {
        "line_id": line.line_id,
        "text": line.line_text,
        "character": line.name,
        "age": line.age,
        "movie": line.title,
        "line_info": {
            "num_words": len(re.findall(r'\w+', line.line_text)),
            "num_sentences": num_sentences,
            "num_total_lines": num_total_lines
        }
    }

    return response
 
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
        "text": db.lines[int(id)].line_text,
        "character": db.characters[db.lines[int(id)].c_id].name,
        "age": db.characters[db.lines[int(id)].c_id].age or None,
        "movie": db.movies[db.lines[int(id)].movie_id].title,
        "line_info": line_info
    }
    """

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

    if sort is line_sort_options.character:
        order_by = db.characters.c.name
    elif sort is line_sort_options.movie:
        order_by = db.movies.c.title
    elif sort is line_sort_options.text:
        order_by = db.lines.c.line_text
    else:
        assert False

    stmt = sqlalchemy.select(
            db.lines.c.line_id,
            db.lines.c.line_text,
            db.movies.c.title,
            db.characters.c.name).select_from(
        db.lines.join(db.movies, db.lines.c.movie_id == db.movies.c.movie_id).join(
        db.characters, db.lines.c.character_id == db.characters.c.character_id)
        ).limit(limit).offset(offset).order_by(order_by, db.lines.c.line_text)
    
    if subtext != "":
        stmt = stmt.where(func.lower(db.lines.c.line_text).ilike(f"%{subtext.lower()}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "line_id": row.line_id,
                    "line_text": row.line_text,
                    "movie": row.title,
                    "character": row.name,
                }
            )
    return json        
            
    
    """
    lines = []

    for line, value in db.lines.items():

        l = {
            "line_id": line,
            "text": value.line_text,
            "movie": db.movies[value.movie_id].title,
            "character": db.characters[value.c_id].name
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
    """

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

    stmt = sqlalchemy.select(
        db.lines.c.line_id,
        db.lines.c.line_text,
        db.movies.c.title,
        db.characters.c.name).select_from(
    db.lines.join(db.movies, db.lines.c.movie_id == db.movies.c.movie_id).join(
    db.characters, db.lines.c.character_id == db.characters.c.character_id)
    )

    if name != "":
        if source == line_source_options.character:
            stmt = stmt.where(func.lower(db.characters.c.name) == name.lower()).limit(limit).offset(offset)
        elif source == line_source_options.movie:
            stmt = stmt.where(func.lower(db.movies.c.title) == name.lower()).limit(limit).offset(offset)
    
    with db.engine.connect() as conn:
        result = conn.execute(stmt)

        json = []
        for row in result:
            json.append(
                {
                    "line_id": row.line_id,
                    "line_text": row.line_text,
                    "movie": row.title,
                    "character": row.name,
                }
            )

    if len(json) == 0:
            if source == line_source_options.character:
                raise HTTPException(422, "Character not found.")
            if source == line_source_options.movie:
                raise HTTPException(422, "Movie not found.")
    return json   
        

    """
    lines = []
    name_found = False

    if source == "character":
        
        for character in db.characters.values():
            if urllib.parse.unquote(name).lower() == character.name.lower():
                id = character.id
                name_found = True
                break

        if name_found == False:
            raise HTTPException(status_code=404, detail="character not found.")    
        
        for l in db.lines.values():
            if l.c_id == id:
                line = {
                    "line_id": l.id,
                    "text": l.line_text,
                    "movie": db.movies[l.movie_id].title,
                    "character": db.characters[id].name
                }
                lines.append(line)

    if source == "movie":

        for movie in db.movies.values():
            if urllib.parse.unquote(name).lower() == movie.title.lower():
                id = movie.id
                name_found = True
                break

        if name_found == False:
            raise HTTPException(status_code=404, detail="movie not found.")    
        
        for l in db.lines.values():
            if l.movie_id == id:
                line = {
                    "line_id": l.id,
                    "text": l.line_text,
                    "movie": db.movies[l.movie_id].title,
                    "character": db.characters[l.c_id].name
                }
                lines.append(line)

    return lines[offset : limit + offset]
    """