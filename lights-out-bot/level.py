'''\
This module provide simple and powerfull tools for level-making.

You can use basic implementation :code:`Level`
or make your custom tool by inheritance of :code:`BaseLevel`.

Example:

>>> level = Level.from_string(4, 3, 'X..X .XX. X.X.', '.', 'X')
>>> level.width
4
>>> level.height
3
>>> print(*level)
True False False True False True True False True False True False

'''

from abc import ABC, abstractmethod

from typing import Container, Iterator, Sequence, TextIO


class BaseLevel(ABC):
	'''\
	Base class for all Level objects.

	You can use it to make custom level object like in the example below:
	
	.. code:: python
		:number-lines: 1

		class MyCustom_AlwaysZeroLevel(BaseLevel):

			def __init__(self, width: int, height: int):
				self._width = width
				self._height = height

			@property
			def width(self) -> int:
				return self._width

			@property
			def height(self) -> int:
				return self._height

			def __iter__(self) -> Iterator[bool]:
				for row in range(self.height):
					for col in range(self.width):
						yield False
		
		level = MyCustom_AlwaysZeroLevel(5, 6)
		assert level.width == 5
		assert level.height == 6
		assert not any(level), 'AlwaysZeroLevel is not always zero! Aaaaaaaaaa!'

	.. NOTE::

		I use :code:`property` for width and height because width and height
		are properties! It's important for level object have an exat private
		info about itself.
	'''

	@property
	@abstractmethod
	def width(self) -> int:
		'''\
		Width of the level.
		'''

		return 0

	@property
	@abstractmethod
	def height(self) -> int:
		'''\
		Height of the level.
		'''
		return 0

	@abstractmethod
	def __iter__(self) -> Iterator[bool]:
		'''\
		Interlacing representation of the level.

		Order of cells: (4 x 4 example)

		+---+---+---+---+
		|1  |2  |3  |4  |
		+---+---+---+---+
		|5  |6  |7  |8  |
		+---+---+---+---+
		|9  |10 |11 |12 |
		+---+---+---+---+
		|13 |14 |15 |16 |
		+---+---+---+---+

		Example: (True and False in replaced to 1 and 0)

		+-+-+-+-+
		|0|1|1|1|
		+-+-+-+-+
		|1|0|1|0|
		+-+-+-+-+
		|0|1|1|0|
		+-+-+-+-+
		|1|0|0|1|
		+-+-+-+-+

		Iterator:

		+----+----+----+----+
		|0111|1010|0110|1001|
		+----+----+----+----+

		.. NOTE::

			The `length` of the iterator should be greater or equal width * height.
		'''

		return
		yield


class Level(BaseLevel):
	'''\
	'''

	@classmethod
	def from_string(
			cls, width: int, height: int, string: str,
			off_codes: Container[str], on_codes: Container[str]
		):

		content = []
		for char in string:
			if char in on_codes:
				content.append(True)
			elif char in off_codes:
				content.append(False)
			# If the char is unknown, it is ignored
		return cls(width, height, content=content)

	@classmethod
	def from_io(cls, io: TextIO):
		width, height, skip = map(int, io.readline().split())
		off_codes = io.readline().strip()
		on_codes = io.readline().strip()
		for i, _ in zip(range(skip), io):
			pass
		return cls.from_string(width, height, io.readline(), off_codes, on_codes)

	@classmethod
	def from_file(cls, filename: str):
		with open(filename) as file:
			return cls.from_io(file)

	def __init__(self, width, height, *, content: Sequence[bool] = tuple()):
		self.__width = width
		self.__height = height
		self.__content = content

	@property
	def width(self) -> int:
		return self.__width

	@property
	def height(self) -> int:
		return self.__height

	def __iter__(self) -> Iterator[bool]:
		yield from self.__content
		for _ in range(self.width * self.height - len(self.__content)):
			yield False

