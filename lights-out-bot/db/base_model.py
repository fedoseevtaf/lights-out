from peewee import SqliteDatabase, Model


db = SqliteDatabase('bot.db')


class BaseModel(Model):

	class Meta():
		database = db

