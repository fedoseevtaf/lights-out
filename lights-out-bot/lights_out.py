import atexit

from game import Game
from level import Level
from user_info import UserInfo

import db


OFF_CODES = '.~o,'
ON_CODES = '#0XO'


class LightsOut():

	@classmethod
	def get_user_info(cls, user_id) -> UserInfo:
		db.db.connect()
		user, created = db.User.get_or_create(id=user_id)
		if user.game is None:
			db.db.close()
			return UserInfo(user_id=user_id)
		game_data = user.game
		game = cls._make_game_from_game_data(game_data)
		info = cls._make_user_info_from_game(user_id, game)
		db.db.close()
		return info

	@classmethod
	def _make_game_from_game_data(cls, game_data: db.Game) -> Game:
		return Game.from_string(
			game_data.width, game_data.height, game_data.field,
			OFF_CODES, ON_CODES
		)

	@classmethod
	def _make_user_info_from_game(cls, user_id: int, game: Game) -> UserInfo:
		return UserInfo(
			user_id=user_id,
			in_game=True,
			width=game.width,
			height=game.height,
			field=tuple(game),
		)












