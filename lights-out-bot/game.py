from level import BaseLevel


class Game(BaseLevel):
	def set_state(self, lvl: BaseLevel):
		self.lvl = list(lvl)
		self._width = lvl.width
		self._height = lvl.height

	def board_action(self, col: int, row: int):
		for y in range(row - 1, row + 2):
			for x in range(col - 1, col + 2):
				number = x * self.width + y
				if 0 <= number <= len(self.lvl):
					self.lvl[number] = not(self.lvl[number])

	@property
	def width(self) -> int:
		'''\
		Level width
		'''

		return self._width

	@property
	def height(self) -> int:
		'''\
		Level height
		'''
		return self._height

	def __iter__(self):
		return iter(self.lvl)

Game()