from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlalchemy
from sqlalchemy import func


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.
    """
    char1_found = False
    char2_found = False

    char_subq = sqlalchemy.select(
        db.characters.c.character_id
        ).select_from(
        db.characters
        ).where(db.characters.c.movie_id == movie_id)
    
    with db.engine.connect() as conn:
        chars = conn.execute(char_subq)
        for char in chars:
            if char.character_id == conversation.character_1_id:
                char1_found = True
            if char.character_id == conversation.character_2_id:
                char2_found = True 
            
    if not char1_found or not char2_found:
        raise HTTPException(422, "Character not part of referenced movie.")    

    
    if conversation.character_1_id == conversation.character_2_id:
        raise HTTPException(status_code=422, detail="Characters are the same.")

    for line in conversation.lines:
        if (line.character_id != conversation.character_1_id and
            line.character_id != conversation.character_2_id):
            raise HTTPException(422, "Characters of lines do not match characters of conversation.")
    
        
    with db.engine.begin() as conn:
        max_id = conn.execute(sqlalchemy.select(func.max(db.conversations.c.conversation_id))).scalar()
        conversation_id = (max_id or 0) + 1
        conn.execute(db.conversations.insert().values(conversation_id = conversation_id,
                                                      movie_id=movie_id,
                                                    character1_id=conversation.character_1_id,
                                                    character2_id=conversation.character_2_id))
        for line in conversation.lines: 
            max_line_id = conn.execute(sqlalchemy.select(func.max(db.lines.c.line_id))).scalar()
            line_id = (max_line_id or 0) + 1
            conn.execute(db.lines.insert().values(line_id = line_id,
                                                  conversation_id=conversation_id,
                                                   character_id=line.character_id,
                                                   line_text=line.line_text))
    return conversation_id

    """

    if (db.characters[conversation.character_1_id].movie_id != movie_id or  
            db.characters[conversation.character_2_id].movie_id != movie_id):
        raise HTTPException(status_code=422, detail="character not in movie.")
    
    if conversation.character_1_id == conversation.character_2_id:
        raise HTTPException(status_code=422, detail="characters are the same.")
    
    for line in conversation.lines:
        if (line.character_id != conversation.character_1_id and
            line.character_id != conversation.character_2_id):
            raise HTTPException(status_code=422, detail="lines do not reference characters.")
        

    next_convo_id = int(db.convos[len(db.convos)-1]["conversation_id"]) + 1

    db.convos.append({"conversation_id": next_convo_id,
                       "character1_id": conversation.character_1_id,
                       "character2_id": conversation.character_2_id,
                       "movie_id": movie_id
                       })
    
    db.upload_new_conversation() # This would fail upon multiple simultaneous calls 
                                 # because the file would be read with one call before 
                                 # the new data is posted in the other call

    line_sort = 1
    for l in conversation.lines:

        next_line_id = int(db.char_lines[len(db.char_lines)-1]["line_id"]) + 1

        db.char_lines.append({"line_id": next_line_id,
                        "character_id": l.character_id,
                        "movie_id": movie_id,
                        "conversation_id": next_convo_id,
                        "line_sort": line_sort,
                        "line_text": l.line_text
                        })
        line_sort += 1
    
    db.upload_new_lines()       # This would fail upon multiple simultaneous calls 
                                # because the file would be read with one call before 
                                # the new data is posted in the other call

    return next_convo_id
    """
