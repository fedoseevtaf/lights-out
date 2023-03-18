import atexit
import json
from typing import Callable


class UserState():
	_init_chat = print
	_storage = {}

	@classmethod
	def set_chat_init_callback(cls, callback: Callable):
		cls._init_chat = callback

	@classmethod
	def update_by_command(cls, user_id, command: str):
		message_id = cls._storage.get(user_id)
		if message_id is None:
			message_id = cls.reset_user_message(user_id)

		content = None
		if command == 'print':
			content = 'Hello, World!'

		return message_id, 'main', content

	@classmethod
	def update_by_message(cls, user_id, message: str):
		message_id = cls._storage.get(user_id)
		if message_id is None:
			message_id = cls.reset_user_message(user_id)

		content = f'message: {message}'
		if 'hello' in message:
			content = 'Hello, World!'

		return message_id, 'main', content

	@classmethod
	def reset_user_message(cls, user_id):
		cls._storage[user_id] = cls._init_chat(user_id)
		return cls._storage[user_id]

