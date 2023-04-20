from conf_level import LEVELS

import db


db.db.connect()
db.db.create_tables([db.Game, db.User, db.Level])
for game_mode, width, height, code in LEVELS:
	db.Level.create(mode=game_mode, width=width, height=height, code=code)
db.db.close()

