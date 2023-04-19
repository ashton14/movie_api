from fastapi import FastAPI
<<<<<<< HEAD
from src.api import characters, movies, lines, pkg_util
=======
from src.api import characters, movies, conversations, pkg_util
>>>>>>> upstream/main

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
* **retreive all lines from a specified source
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
        "description": "Access information on lines in movies.",
    }
]

app = FastAPI(
    title="Movie API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Ashton Alonge",
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
