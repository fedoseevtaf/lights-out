from conf_level import LEVELS

import db


def create_tables():
	db.db.create_tables([db.Game, db.User, db.Level])


def create_levels():
	for game_mode, width, height, code in LEVELS:
		db.Level.create(mode=game_mode, width=width, height=height, code=code)


if __name__ == '__main__':
	db.db.connect()
	create_tables()
	create_levels()
	db.db.close()

