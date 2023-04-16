from peewee import *

from db.base_model import BaseModel
from db.game import Game


class User(BaseModel):

	id = IntegerField(primary_key=True)
	game = ForeignKeyField(Game, backref='user', null=True, default=None)

