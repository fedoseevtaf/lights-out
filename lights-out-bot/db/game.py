from peewee import (
	IntegerField, CharField, DateTimeField, ForeignKeyField,
	Check,
)

from db.base_model import BaseModel
from db.level import Level


class Game(BaseModel):

	width = IntegerField(constraints=[Check('width >= 3')])
	height = IntegerField(constraints=[Check('height >= 3')])
	field = CharField()

	move_n = IntegerField()
	start_time = DateTimeField()
	level_id = ForeignKeyField(Level, backref='+')

