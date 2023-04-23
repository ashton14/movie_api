from fastapi import FastAPI
from src.api import characters, movies, conversations, lines, pkg_util

description = """
Movie API returns dialog statistics on top hollywood movies from decades past.

## Characters

You can:
* **list characters with sorting and filtering options.**
* **retrieve a specific character by id**

## Movies

You can:
* **list movies with sorting and filtering options.**
* **retrieve a specific movie by id**

## Lines

You can:
* **list lines with sorting and filtering options.**
* **retrieve a specific line by id**
* **list lines from a specific source
"""
tags_metadata = [
    {
        "name": "characters",
        "description": "Access information on characters in movies.",
    },
    {
        "name": "movies",
        "description": "Access information on top-rated movies.",
    },
    {
        "name": "lines",
        "description": "Access information on lines from movies.",
    }
]

app = FastAPI(
    title="Movie API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Ashton",
        "email": "aalonge@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(characters.router)
app.include_router(movies.router)
app.include_router(lines.router)
app.include_router(pkg_util.router)
app.include_router(conversations.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API. See /docs for more information."}