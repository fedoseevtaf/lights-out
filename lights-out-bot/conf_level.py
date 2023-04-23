from random_level import RandomLevel
from level import Level


LEVELS = {
	('random', 5, 5, ''): RandomLevel(5, 5),
	('random', 3, 3, ''): RandomLevel(3, 3),
	('random', 4, 4, ''): RandomLevel(4, 4),
	('random', 6, 6, ''): RandomLevel(6, 6),
	('random', 7, 7, ''): RandomLevel(7, 7),

	('level', 5, 5, '1'): Level.from_file('levels/classic_5_5_1.lvl'),
	('level', 5, 5, '2'): Level.from_file('levels/classic_5_5_2.lvl'),
	('level', 5, 5, '3'): Level.from_file('levels/classic_5_5_3.lvl'),
	('level', 5, 5, '4'): Level.from_file('levels/classic_5_5_4.lvl'),
	('level', 5, 5, '5'): Level.from_file('levels/classic_5_5_5.lvl'),
	('level', 5, 5, '6'): Level.from_file('levels/classic_5_5_6.lvl'),
	('level', 5, 5, '7'): Level.from_file('levels/classic_5_5_7.lvl'),
	('level', 5, 5, '8'): Level.from_file('levels/classic_5_5_8.lvl'),
	('level', 5, 5, '9'): Level.from_file('levels/classic_5_5_9.lvl'),
	('level', 5, 5, '10'): Level.from_file('levels/classic_5_5_10.lvl'),
	('level', 5, 5, '11'): Level.from_file('levels/classic_5_5_11.lvl'),
	('level', 5, 5, '12'): Level.from_file('levels/classic_5_5_12.lvl'),
	('level', 5, 5, '13'): Level.from_file('levels/classic_5_5_13.lvl'),
	('level', 5, 5, '14'): Level.from_file('levels/classic_5_5_14.lvl'),
	('level', 5, 5, '15'): Level.from_file('levels/classic_5_5_15.lvl'),
}
