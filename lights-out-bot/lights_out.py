from typing import NoReturn, Optional
import datetime

import peewee

from game import Game

from user_info import UserInfo

from conf_level import LEVELS

import db


OFF_CODES = '.~o,'
ON_CODES = '#0XO'


class LightsOut():

	@classmethod
	def get_user_info(cls, user_id) -> UserInfo:
		db.db.connect()
		user, created = db.User.get_or_create(id=user_id)
		game_data = user.game
		if game_data is not None:
			game = cls._make_game_from_game_data(game_data)
			info = cls._make_user_info_from_game(user_id, game)
		else:
			info = UserInfo(user_id=user_id)
		db.db.close()
		return info

	@classmethod
	def start_game(
			cls, user_id: int,
			game_mode: str,
			width: int, height: int,
			level_code: str,
		) -> NoReturn:
		game = cls._make_game(game_mode, width, height, level_code)
		if game is None:
			return
		db.db.connect()
		level_data = cls._extract_level_data(game_mode, width, height, level_code)
		if level_data is None:
			db.db.close()
			return
		game_data = db.Game.create(
			width=width, height=height, field=game.to_string(OFF_CODES, ON_CODES),
			move_n=0, start_time=datetime.datetime.now(), level_id=level_data.id,
		)
		db.User.update(game=game_data).where(db.User.id == user_id).execute()
		db.db.close()

	@classmethod
	def quit_game(cls, user_id):
		db.db.connect()
		user = db.User.get(id=user_id)
		user.game.delete_instance()
		user.game = None
		user.save()
		db.db.close()

	@classmethod
	def board_action(cls, user_id: int, row: int, col: int):
		db.db.connect()
		user = db.User.select().where(db.User.id == user_id).get()
		game_data = user.game
		game = Game.from_string(
			game_data.width, game_data.height, game_data.field,
			OFF_CODES, ON_CODES,
		)
		is_valid = game.board_action(row, col)
		if is_valid:
			game_data.move_n += 1
		game_data.field = game.to_string(OFF_CODES, ON_CODES)
		game_data.save()
		db.db.close()
		return game.win

	@classmethod
	def _make_game(
			cls, game_mode: str,
			width: int, height: int,
			level_code: str,
		) -> Optional[Game]:
		level = LEVELS.get((game_mode, width, height, level_code))
		if level is None:
			return
		return Game(width, height, content=tuple(level))

	@classmethod
	def _extract_level_data(
			cls, game_mode: str,
			width: int, height: int,
			level_code: str,
		) -> Optional[db.Level]:
		try:
			return db.Level.get(
				mode=game_mode, width=width, height=height, code=level_code,
			)
		except peewee.DoesNotExist:
			return

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
			board=tuple(game),
		)

