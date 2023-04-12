import atexit

from game import Game
from level import Level
from user_info import UserInfo


DUMP = 'dump.tmp'


class LightsOut():
	_game = Game()

	_storage = {}
	try:
		with open(DUMP) as file:
			_storage = eval(file.read())
	except Exception:
		pass

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
	def board_action(cls, user_id, row: int, col: int) -> UserInfo:
		info = cls.get_user_info(user_id)
		if not info.in_game:
			return info

		level = Level(info.width, info.height, content=info.board)
		cls._game.set_state(level)
		cls._game.board_action(row, col)
		new_info = UserInfo(
			user_id=info.user_id,
			in_game=info.in_game,
			board=tuple(cls._game),
			width=cls._game.width,
			height=cls._game.height,
		)
		cls._storage[user_id] = new_info
		return new_info

	@classmethod
	def _build_info(cls, user_id) -> UserInfo:
		return UserInfo(
			user_id=user_id,
			in_game=False,
			board=(
				True, False, True, True, False,
				False, True, True, True, False,
				True, True, True, False, False,
				True, True, False, True, True,
				False, False, False, True, True,
			),
			width=5, height=5,
		)

