from peewee import *


db = SqliteDatabase('bot.db')


class BaseModel(Model):

	class Meta():
		database = db

