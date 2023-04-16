from random import random
from typing import Iterator, NoReturn

from level import BaseLevel


class RandomLevel(BaseLevel):

	def __init__(self, width: int, height: int) -> NoReturn:
		self._width = width
		self._height = height

	@property
	def width(self) -> int:
		return self._width

	@property
	def height(self) -> int:
		return self._height

	def __iter__(self) -> Iterator[bool]:
		return (
			random() > 0.5
			for _ in range(self.width)
				for _ in range(self.height)
		)

