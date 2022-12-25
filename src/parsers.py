import aiohttp
import calendar
import datetime
from abc import ABC, abstractmethod

from .movie import MoviesList, Movie
from .constants import TOP_K_FILMS


class BaseParser(ABC):

    @abstractmethod
    async def parse_pack_of_movies(self, query: str) -> MoviesList:
        pass

    @abstractmethod
    async def parse_movie_by_id(self, id: int) -> Movie:
        pass

    @abstractmethod
    async def parse_similars(self, id: int) -> MoviesList:
        pass


class KinopoiskParser(BaseParser):

    def __init__(
        self, 
        api_key_token: str,
        kinopoisk_search_api_end_point: str, 
        kinopoisk_by_id_api_end_point: str,
        kinoposik_similars_api_end_point: str,
    ):
        self._api_key_token = api_key_token
        self._kinopoisk_search_api_end_point = kinopoisk_search_api_end_point
        self._kinopoisk_by_id_api_end_point = kinopoisk_by_id_api_end_point
        self._kinopoisk_similars_api_end_point = kinoposik_similars_api_end_point

    async def parse_pack_of_movies(self, query: str) -> MoviesList | None:
        header = {
            'X-API-KEY': self._api_key_token,
            'accept': 'application/json',
        }
        params = {
            'keyword': query,
        }
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(self._kinopoisk_search_api_end_point, params=params) as response:
                json_response = await response.json()
                return self._parse_json_pack_movies(json_response)

    async def parse_movie_by_id(self, id: int) -> Movie:
        header = {
           'X-API-KEY': self._api_key_token,
           'accept': 'application/json', 
        }
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(self._kinopoisk_by_id_api_end_point + str(id)) as response:
                json_response = await response.json()
                return self._parse_json_movie(json_response)

    async def parse_similars(self, id: int) -> MoviesList:
        header = {
            'X-API-KEY': self._api_key_token,
            'accept': 'application/json',  
        }
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(self._kinopoisk_similars_api_end_point + str(id) + "/similars") as response:
                json_response = await response.json()
                json_response["films"] = json_response["items"]
                return self._parse_json_pack_movies(json_response)

    @staticmethod
    def _parse_json_pack_movies(movies_json: dict[str, str]) -> MoviesList | None:
        if not len(movies_json["films"]):
            return None

        movies_list: list[Movie] = []
        for film in movies_json["films"][:TOP_K_FILMS]:
            movies_list.append(
                Movie(
                    name=film["nameRu"],
                    year=film["year"] if "year" in film else "",
                    countries=[x["country"] for x in film["countries"]] if "countries" in film else "",
                    id=film["filmId"]
                )
            )
        return MoviesList(movies_list)

    @staticmethod
    def _parse_json_movie(movie_json: dict[str, str]) -> Movie:
        return Movie(
            name=movie_json["nameRu"],
            year=movie_json["year"],
            countries=[x["country"] for x in movie_json["countries"]],
            id=movie_json["kinopoiskId"] ,
            genres=[g["genre"] for g in movie_json["genres"]],
            rating_imdb=movie_json["ratingImdb"],
            rating_kinopoisk=movie_json["ratingKinopoisk"],
            short_description=movie_json["description"],
            poster_url=movie_json["posterUrlPreview"]
        )


class IMDBParser(BaseParser):
    pass
