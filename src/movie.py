from dataclasses import dataclass, field


@dataclass
class Movie:
    name: str
    year: int
    countries: list[str]
    id: int
    genres: list[str] = field(default_factory=list)
    rating_imdb: float = 0.0
    rating_kinopoisk: float = 0.0
    short_description: str = ""
    poster_url: str = ""

@dataclass
class MoviesList:
    movies: list[Movie]