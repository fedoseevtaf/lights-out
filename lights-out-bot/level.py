'''\
This module provides simple and powerfull tools for creating levels.

You can use basic implementation :code:`Level`
or make your custom tool by inheriting from :code:`BaseLevel`.

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

		I use :code:`property` for width and height
	'''

	@property
	@abstractmethod
	def width(self) -> int:
		'''\
		Level width
		'''

		return 0

	@property
	@abstractmethod
	def height(self) -> int:
		'''\
		Level height
		'''
		return 0

	@abstractmethod
	def __iter__(self) -> Iterator[bool]:
		'''\
		Line by line representation of the level.

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

			The `length` of the iterator should be greater or equal than :strong:`width * height`
		'''

		return
		yield


class Level(BaseLevel):
	'''\
	This is a basic implementation for level.

	It have built-in functions to load level from different sources.

	1. Prepared :code:`Sequence[bool]`
		>>> level_content = (
				True, False, False, True,
				False, True, True, False,
				True, False, True, False,
		)
		>>> level = Level(4, 3, content=level_content)
	2. String
		>>> level_content = \'''\
		X..X
		.XX.
		X.X.
		\'''
		>>> level = Level.from_string(4, 3, level_content, '.', 'X')
	3. File (:code:`TextIO`)
		.. NOTE::

			Text io data must be written in special format

		>>> level_content = \'''\
		4 3 0
		.*
		X#
		#..X	.#X*	X*X.
		\'''
		>>> import io
		>>> level = Level.from_io(io.StringIO(level_content))

	After that you get a simple level object.
	>>> level.width
	4
	>>> level.height
	3
	>>> print(*level)
	True False False True False True True False True False True False
	'''

	@classmethod
	def from_string(
			cls, width: int, height: int, string: str,
			off_codes: Container[str], on_codes: Container[str]
		):
		'''\
		Read level from string.

		:width:
			level width
		:height:
			level height
		:string:
			string of level (rows aren't separated)
		:off_codes:
			:code:`Container` of the **light-off** characters
		:on_codes:
			:code:`Container` of the **light-on** characters

		.. NOTE::

			If character in string isn't in :code:`on/off_codes` it's ignored
		'''

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
		'''\
		Read level from io (use a special format).

		:io:
			:code:`TextIO` to read level
		'''

		width, height, skip = map(int, io.readline().split())
		off_codes = io.readline().strip()
		on_codes = io.readline().strip()
		for i, _ in zip(range(skip), io):
			pass
		return cls.from_string(width, height, io.readline(), off_codes, on_codes)

	@classmethod
	def from_file(cls, filename: str):
		'''\
		:filename:
			file name

		The same as:

		.. code:: python

			with open(filename) as file:
				return cls.from_io(file)
		'''

		with open(filename) as file:
			return cls.from_io(file)

	def __init__(self, width, height, *, content: Sequence[bool] = tuple()):
		'''\
		:width:
			level width
		:height:
			level height
		:content:
			Prepared :code:`Sequence[bool]`
		'''

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
		'''\
		Line by line representation of the level.

		.. NOTE::

			If the content `length` isn't enough it yields False
		'''

		yield from self.__content
		for _ in range(self.width * self.height - len(self.__content)):
			yield False

