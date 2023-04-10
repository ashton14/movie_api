from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()

def topCharacters(id: str):

    top_characters = []
    for character, value in db.characters.items():
        if value[1] == id:
            char = {
                "character_id": character,
                "character": value[0],
                "num_lines": num_lines(id, character)
            }

            top_characters.append(char)

    return get_top_five(top_characters)


def num_lines(movie_id: str, character_id: str):

    numLines = 0

    for line in db.lines.values():
        if line[1] == movie_id and line[0] == character_id:
            numLines += 1

    return numLines


def get_top_five(characters: list):

    top_characters = []
    sorted_list = sorted(characters, key=lambda x: x["num_lines"], reverse=True)

    for i in range(5):
        top_characters.append(sorted_list[i])

    return reversed(top_characters)


# include top 5 actors by number of lines
@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: str):
    """
    This endpoint returns a single movie by its identifier. For each movie it returns:
    * `movie_id`: the internal id of the movie.
    * `title`: The title of the movie.
    * `top_characters`: A list of characters that are in the movie. The characters
      are ordered by the number of lines they have in the movie. The top five
      characters are listed.

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `num_lines`: The number of lines the character has in the movie.

    """

    
    json =  {
        "movie_id": id,
        "title": db.movies[id][0],
        "top_characters": topCharacters(id)
    }

    json = None

    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return json


class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"


# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    """
    This endpoint returns a list of movies. For each movie it returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movies/{movie_id}` endpoint.
    * `movie_title`: The title of the movie.
    * `year`: The year the movie was released.
    * `imdb_rating`: The IMDB rating of the movie.
    * `imdb_votes`: The number of IMDB votes for the movie.

    You can filter for movies whose titles contain a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `movie_title` - Sort by movie title alphabetically.
    * `year` - Sort by year of release, earliest to latest.
    * `rating` - Sort by rating, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    json = None

    return json
