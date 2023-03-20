from dataclasses import dataclass
from typing import Tuple


@dataclass(kw_only=True)
class UserInfo():
	user_id: int
	in_game: bool = False
	width: int = 0
	height: int = 0
	board: Tuple[int] = tuple()

