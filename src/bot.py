from aiogram import Bot, types

from .constants import START_MSG, HELP_MSG, ERR_TRY_MSG, KP_MAX_ID
from .movie import MoviesList, Movie
from .parsers import KinopoiskParser


class TgBot:
    def __init__(self, bot: Bot, parser: KinopoiskParser) -> None:
        self._bot = bot
        self._parser = parser
    
    async def search_handler(self, message: types.Message) -> None:
        parsed_movies_pack = await self._parser.parse_pack_of_movies(message.get_args())
        movies_pack_message = self._create_movies_pack_message(parsed_movies_pack)
        await self._bot.send_message(message.chat.id, movies_pack_message, parse_mode="Markdown")
    
    async def search_by_id_handler(self, message: types.Message) -> None:
        kp_id = int(message.text[3:])
        if (kp_id >= KP_MAX_ID) or (kp_id < 0):
            self._bot.send_message(message.chat.id, ERR_TRY_MSG)

        parsed_movie = await self._parser.parse_movie_by_id(kp_id)
        movie_message = self._create_movie_description_message(parsed_movie)
        if parsed_movie.poster_url:
            await self._bot.send_photo(message.chat.id, photo=parsed_movie.poster_url, caption=movie_message, parse_mode="Markdown")
        else:
            await self._bot.send_message(message.chat.id, movie_message, parse_mode="Markdown")
        #TODO:  write to db

    async def similars_by_id_handler(self, message: types.Message) -> None:
        kp_id = int(message.text[4:])
        if (kp_id >= KP_MAX_ID) or (kp_id < 0):
            self._bot.send_message(message.chat.id, ERR_TRY_MSG)
        
        parsed_movies_pack = await self._parser.parse_similars(kp_id)
        movies_pack_message = self._create_movies_pack_message(parsed_movies_pack)
        movies_pack_message = f"Похожие на /id{kp_id}\n" + movies_pack_message
        await self._bot.send_message(message.chat.id, movies_pack_message, parse_mode="Markdown") 

    async def start_handler(self, message: types.Message) -> None:
        await self._bot.send_message(message.chat.id, START_MSG, parse_mode="Markdown")
    
    async def help_handler(self, message: types.Message) -> None:
        await self._bot.send_message(message.chat.id, HELP_MSG, parse_mode="Markdown")

    @staticmethod
    def _create_movies_pack_message(pack: MoviesList | None) -> str:
        if pack is None:
            return ERR_TRY_MSG

        message = "Вот, что я нашел по твоему запросу.\n"
        for i, film in enumerate(pack.movies):
            year_and_countries = ""
            if len(film.year) and len(film.countries):
                year_and_countries = f"_({film.year}, {', '.join(film.countries)})_"
            message += f"{i + 1}. *{film.name}* {year_and_countries if len(year_and_countries) else ''}\n/id{film.id}\n"
        message += "Для того, чтобы получить подробную информацию о фильме нажми на `/id{идентификатор}` рядом."
        return message

    @staticmethod
    def _create_movie_description_message(movie: Movie) -> str:
        message = ""
        message += f"*{movie.name}* (_{movie.year}, {', '.join(movie.countries)}_)\n\n"
        message += f"*Жанр:* {', '.join(movie.genres)}\n\n"
        message += f"*Кинопоиск:* {movie.rating_kinopoisk}\n*IMDB:* {movie.rating_imdb}\n\n"
        message += movie.short_description + "\n\n"
        if len(message) >= 950:
            message = message[:950] + "...\n\n"
        message += f"Посмотреть похожие: /sim{movie.id}"
        return message
