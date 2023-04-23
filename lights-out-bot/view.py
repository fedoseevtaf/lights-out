import telebot.types as tp

from view_const import PAGE, PAGE_TEXT, PAGE_REPLY_BUTTONS


class MessageConstructor:

	@classmethod
	def make_text(cls, page_id, content):
		return choice(PAGE_TEXT.get(page_id, 'None'))

	@classmethod
	def make_markup(cls, page_id, content):
		if page_id is PAGE.GAME:
			return cls._make_game_markup(content)
		markup = tp.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add(*(
			tp.KeyboardButton(text_btn)
			for text_btn in PAGE_REPLY_BUTTONS[page_id]
		))
		return markup

	@classmethod
	def _make_game_markup(cls, content):
		markup = tp.InlineKeyboardMarkup(row_width=content['width'])
		markup.add(*(
			tp.InlineKeyboardButton(
				('⬜' if btn else '⬛'),
				callback_data=(
						'{"row":' +
						str(ind // content['width']) +
						', "col": ' +
						str(ind % content['width']) + '}'
				)
			)
			for ind, btn in enumerate(content['board'])
		))
		markup.add(tp.InlineKeyboardButton('Сдаюсь', callback_data='quit'))
		return markup

