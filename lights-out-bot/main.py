"""\
Main module contains bot api manipulation.
Other modules user high abstraction level with just user_id and message_id,
for message identification and handling.
"""


from os import environ
from typing import Any, Dict, NoReturn, Optional

import telebot as tb
import telebot.types as tp

# Main modules import
from user_state import UserState
from view import MessageConstructor
# Conf modules import
from view_const import PAGE_COMMANDS
from logging_conf import log


API_TOKEN = environ['TGBOT_TOKEN']

bot = tb.TeleBot(API_TOKEN)


@UserState.set_hide_message_callback
def delete_message(chat_id: int, message_id: int) -> NoReturn:
	"""\
	Function is provided for the UserState for message managment.
	"""

	bot.delete_message(chat_id, message_id)


@UserState.set_show_message_callback
def send_message(
		# Message specification
		chat_id: int,
		message_id: int,
		in_place: bool = False,
		# Content specification
		page_id: Any = None,
		content: Optional[Dict] = None,
		only_markup: bool = False,
	) -> int:
	"""\
	Function is provided for the UserState for message managment.
	Return id of the new message (that has been edited if `in_place`).
	"""

	if content is None:
		content = {}
	text = MessageConstructor.make_text(page_id, content)
	markup = MessageConstructor.make_markup(page_id, content)
	document = MessageConstructor.make_document(page_id, content)
	return show_message(
		chat_id, message_id, in_place,
		text, markup, only_markup, document,
	)


def show_message(
		# Message specification
		chat_id: int,
		message_id: int,
		in_place: bool = False,
		# Content
		text: str = 'LightsOut!',
		markup: Optional[tb.REPLY_MARKUP_TYPES] = None,
		only_markup: bool = False,
		document: Optional[tp.InputFile] = None,
	) -> int:
	"""\
	Message sending api manipulations. Return message id.
	If `in_place` is True, but there is no message with this message_id,
	new message will be created and returned it is id.
	"""

	if not in_place:
		new_message = send_msg(chat_id, text, markup, document)
		return new_message.message_id

	try:
		if not only_markup:
			bot.edit_message_text(text, chat_id, message_id)
		bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)
	except tb.apihelper.ApiTelegramException as ex:
		if ex.description == 'Bad Request: message to edit not found':
			new_message = send_msg(chat_id, text, markup, document)
			return new_message.message_id
	return message_id


def send_msg(chat_id: int, text, markup, document):
	if document is not None:
		return bot.send_photo(chat_id, document, caption=text, reply_markup=markup)
	return bot.send_message(chat_id, text, reply_markup=markup)


class CommandHandler:
	"""\
	Incapsulate command name.
	"""

	@classmethod
	def _for(cls, command_name: str) -> 'Self':  # 3.10
		"""\
		Make handler for specific command and register it by bot.
		"""

		handler = cls(command_name)
		return bot.message_handler(commands=[command_name])(handler)

	def __init__(self, command_name: str) -> NoReturn:
		self._command_name = command_name

	def __call__(self, message: tp.Message) -> NoReturn:
		log.info(f'Command recieved {self._command_name=}')
		UserState.update_by_command(
			message.chat.id,
			message.message_id,
			self._command_name,
		)
		log.info(f'Command processed {self._command_name=}')


command_handlers: Dict[str, CommandHandler] = {
	cmd: CommandHandler._for(cmd)
	for commands in PAGE_COMMANDS.values()
		for cmd in commands
}


@bot.callback_query_handler(func=lambda query: True)
def handle_callback(query: tp.CallbackQuery):
	"""\
	Throw callback data to the UserState.
	"""

	message = query.message
	log.info('Callback recieved')
	UserState.update_by_callback(message.chat.id, message.message_id, query.data)
	log.info('Callback processed')


# All text messages
@bot.message_handler()
def handle_message(message: tp.Message):
	"""\
	Throw message to the UserState.
	"""

	UserState.update_by_message(message.chat.id, message.message_id, message.text)


# All non text messages
@bot.message_handler(content_types=[
	'audio', 'photo', 'voice', 'video',
	'document', 'location', 'contact', 'sticker'
])
def handle_spam(message: tp.Message):
	"""\
	Delete unprocessable messages.
	"""

	bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
	bot.infinity_polling()

