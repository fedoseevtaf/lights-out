from dataclasses import dataclass
from typing import Tuple


@dataclass()
class UserInfo:
	user_id: int
	in_game: bool = False
	width: int = 0
	height: int = 0
	board: Tuple[int] = tuple()

