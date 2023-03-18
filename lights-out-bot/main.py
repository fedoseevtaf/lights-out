from os import environ

import telebot as tb
import telebot.types as tp

from user_state import UserState
from view import MessageConstructor


API_TOKEN = environ['TGBOT_TOKEN']

bot = tb.TeleBot(API_TOKEN)


@UserState.set_chat_init_callback
def make_main_message_in_chat(chat_id):
	'''\
	Bot use a single message for user interactions.
	'''

	message = bot.send_message(chat_id, 'Wait please')
	return message.message_id


def edit_message(chat_id, message_id, text, markup):
	bot.edit_message_text(text, chat_id, message_id)
	bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)


class CommandHandler():

	@classmethod
	def _for(cls, command_name: str):
		handler = cls(command_name)
		return bot.message_handler(commands=[command_name])(handler)

	def __init__(self, command_name: str):
		self._command_name = command_name

	def __call__(self, message: tp.Message):
		chat_id = message.chat.id
		bot.delete_message(chat_id, message.message_id)

		(
			message_id,
			page_id,
			content,
		) = UserState.update_by_command(chat_id, self._command_name)
		text = MessageConstructor.make_text(page_id, content)
		markup = MessageConstructor.make_markup(page_id, content)

		try:
			edit_message(chat_id, message_id, text, markup)
		except tb.apihelper.ApiTelegramException as ex:
			if ex.description == 'Bad Request: message to edit not found':
				message_id = UserState.reset_user_message(chat_id)
			edit_message(chat_id, message_id, text, markup)


cmd_print = CommandHandler._for('print')


# All text messages
@bot.message_handler()
def handle_message(message: tp.Message):
	chat_id = message.chat.id
	text = message.text
	bot.delete_message(message.chat.id, message.message_id)

	message_id, page_id, content = UserState.update_by_message(chat_id, text)
	text = MessageConstructor.make_text(page_id, content)
	markup = MessageConstructor.make_markup(page_id, content)

	try:
		edit_message(chat_id, message_id, text, markup)
	except tb.apihelper.ApiTelegramException as ex:
		if ex.description == 'Bad Request: message to edit not found':
			message_id = UserState.reset_user_message(chat_id)
		edit_message(chat_id, message_id, text, markup)


# All non text messages
@bot.message_handler(content_types=[
	'audio', 'photo', 'voice', 'video',
	'document', 'location', 'contact', 'sticker'
])
def handle_message(message: tp.Message):
	bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
	bot.infinity_polling()

