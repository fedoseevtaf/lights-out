import telebot.types as tp


class MessageConstructor():

	@classmethod
	def make_text(cls, page_id, content):
		return f'{content=}'

	@classmethod
	def make_markup(cls, page_id, content):
		markup = tp.InlineKeyboardMarkup()
		button = tp.InlineKeyboardButton(f'{page_id=}', callback_data='qwerty')
		markup.add(button)
		return markup

