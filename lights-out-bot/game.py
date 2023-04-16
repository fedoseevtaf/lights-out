from level import Level


class Game(Level):

	def board_action(self, col: int, row: int):
		for x in range(row - 1, row + 2):
			for y in range(col - 1, col + 2):
				number = y * self.width + x
				if not (0 <= y < self.height) or not (0 <= x < self.width):
					continue
				if col == y or row == x:
					self._content[number] = not self._content[number]

	@property
	def win(self):
		return not any(self)

