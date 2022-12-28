import os
from flask import Flask, render_template, request

from src.movie import Movie, MoviesList
from src.parsers import KinopoiskParser
from src.constants import KP_SEARCH_END_POINT, KP_MOVIE_BY_ID_END_POINT, KP_SIMILARS_END_POINT

parser = KinopoiskParser(
    api_key_token=os.environ['KINO_API_KEY_TOKEN'],
    kinopoisk_search_api_end_point=KP_SEARCH_END_POINT,
    kinopoisk_by_id_api_end_point=KP_MOVIE_BY_ID_END_POINT,
    kinoposik_similars_api_end_point=KP_SIMILARS_END_POINT
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/movies", methods=["GET", "POST"])
async def movies():
    if request.method == "POST":
        to_search = request.form.get("name")
        pack: MoviesList = await parser.parse_pack_of_movies(str(to_search))

        movies_to_render: list[Movie] = []
        for m in pack.movies:
            m_info = await parser.parse_movie_by_id(m.id)
            movies_to_render.append(m_info)

        return render_template("movies.html", movies_to_render=movies_to_render)
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=16135)

