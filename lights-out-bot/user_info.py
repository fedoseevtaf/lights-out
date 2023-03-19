from typing import Tuple


class UserInfo():

	def __init__(self, *,
			user_id: int,
			last_message_id: int = -1,
			in_game: bool = False,
			width: int = 0,
			height: int = 0,
			board: Tuple[int] = tuple(),
		):
		self.user_id = user_id
		self.last_message_id = last_message_id
		self.in_game = in_game
		self.width = width
		self.height = height

