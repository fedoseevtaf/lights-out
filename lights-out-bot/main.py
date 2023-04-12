from os import environ
from typing import Dict, Optional

import telebot as tb
import telebot.types as tp

from user_state import UserState
from view import MessageConstructor


API_TOKEN = environ['TGBOT_TOKEN']

bot = tb.TeleBot(API_TOKEN)


@UserState.set_hide_message_callback
def delete_message(chat_id, message_id):
	bot.delete_message(chat_id, message_id)


@UserState.set_show_message_callback
def send_message(
		# Message specification
		chat_id: int,
		message_id: int,
		in_place: bool,
		# Content specification
		page_id: str,
		content: Optional[Dict] = None,
	):
	if content is None:
		content = {}
	text = MessageConstructor.make_text(page_id, content)
	markup = MessageConstructor.make_markup(page_id, content)
	return show_message(chat_id, message_id, in_place, text, markup)


def show_message(
		# Message specification
		chat_id: int,
		message_id: int,
		in_place: bool = False,
		# Content
		text: str = 'LightsOut!',
		markup: Optional[tb.REPLY_MARKUP_TYPES] = None,
	):
	if not in_place:
		new_message = bot.send_message(chat_id, text, reply_markup=markup)
		return new_message.message_id

	try:
		bot.edit_message_text(text, chat_id, message_id)
		bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)
	except tb.apihelper.ApiTelegramException as ex:
		if ex.description == 'Bad Request: message to edit not found':
			new_message = bot.send_message(chat_id, text, reply_markup=markup)
			return new_message.message_id
	return message_id


class CommandHandler():

	@classmethod
	def _for(cls, command_name: str):
		handler = cls(command_name)
		return bot.message_handler(commands=[command_name])(handler)

	def __init__(self, command_name: str):
		self._command_name = command_name

	def __call__(self, message: tp.Message):
		UserState.update_by_command(
			message.chat.id,
			message.message_id,
			self._command_name,
		)


command_back = CommandHandler._for('back')


@bot.callback_query_handler(func=lambda query: True)
def handle_callback(query):
	message = query.message
	UserState.update_by_callback(message.chat.id, message.message_id, query.data)


# All text messages
@bot.message_handler()
def handle_message(message: tp.Message):
	UserState.update_by_message(message.chat.id, message.message_id, message.text)


# All non text messages
@bot.message_handler(content_types=[
	'audio', 'photo', 'voice', 'video',
	'document', 'location', 'contact', 'sticker'
])
def handle_spam(message: tp.Message):
	bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
	bot.infinity_polling()

