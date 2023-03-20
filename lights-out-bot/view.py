import telebot.types as tp


class MessageConstructor():

	@classmethod
	def make_text(cls, page_id, content):
		return f'{page_id=}\n\n{content=}'

	@classmethod
	def make_markup(cls, page_id, content):
		 markup = tp.InlineKeyboardMarkup()
		 markup.add(tp.InlineKeyboardButton('blabla', callback_data='{\'row\': 0, \'col\': 0}'))
		 return markup

