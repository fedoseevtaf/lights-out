import atexit
from typing import Dict, NewType

from game import Game
from level import Level
from user_info import UserInfo


DUMP = 'file.dump'


class LightsOut():
	_game = Game()

	_storage = {}
	try:
		with open(DUMP) as file:
			_storage = eval(file.read())

	@atexit.register
	def _dump():
		with open(DUMP, 'w') as file:
			file.write(str(LightsOut._storage))

	@classmethod
	def get_user_info(cls, user_id) -> UserInfo:
		info = cls._storage.get(user_id)
		if info is None:
			info = cls._build_info(user_id)
			cls._storage[user_id] = info
		return info

	@classmethod
	def _build_info(cls, user_id) -> UserInfo:
		return UserInfo(
			user_id=user_id,
			in_game=True,
			board=(
				True, False, True, True, False,
				False, True, True, True, False,
				True, True, True, False, False,
				True, True, False, True, True,
				False, False, False, True, True,
			),
			width=5, height=5,
		)

	@classmethod
	def update_message_id(cls, user_id, message_id):
		info = cls.get_user_info()
		new_info = UserInfo(
			user_id=info.user_id,
			last_message_id=message_id,
			in_game=info.in_game,
			width=info.width,
			height=info.height,
			board=info.board,
		)
		cls._storage[user_id] = new_info
		return new_info

	@classmethod
	def board_action(cls, user_id, row: int, col: int) -> UserInfo:
		info = cls.get_user_info(user_id)
		if not info.in_game:
			return info

		level = Level(info.width, info.height, info.board)
		cls._game.set_state(level)
		cls._game.board_action(row, col)
		new_info = UserInfo(
			user_id=info.user_id,
			last_message_id=info.last_message_id,
			in_game=info.in_game,
			board=tuple(cls._game),
			width=cls._game.width,
			height=cls._game.height,
		)
		cls._storage[user_id] = new_info
		return new_info

