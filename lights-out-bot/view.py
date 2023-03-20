import telebot.types as tp

from view_const import MESSAGES_BOT, TEXT_BUTTON


class MessageConstructor:

	@classmethod
	def make_text(cls, page_id, content):
		return MESSAGES_BOT[page_id]

	@classmethod
	def make_markup(cls, page_id, content):
		markup = tp.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add(tp.KeyboardButton(text_btn) for text_btn in TEXT_BUTTON[page_id])
		if page_id == 'game':
			markup = tp.InlineKeyboardMarkup(row_width=content[width])
			markup.add(*(tp.InlineKeyboardButton(
					'⬜' if btn else '⬛',
					callback_data=(
							'{"row":' +
							str(ind // content[width]) +
							', "col": ' +
							str(ind % content[width]) + '}'
					)
				)
				for ind, btn in enumerate(content[board])
				)
			)
		return markup

	@classmethod
	def make_board(cls, page_id):
		pass
