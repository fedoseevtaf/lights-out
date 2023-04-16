from peewee import *

from db.base_model import BaseModel


class Level(BaseModel):

	mode = CharField()
	width = IntegerField()
	height = IntegerField()
	code = CharField()

