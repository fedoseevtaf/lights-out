from base_model import db

from game import Game
from user import User
from level import Level


db.connect()
db.create_tables([Game, User, Level])
db.close()

