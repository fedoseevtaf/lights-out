from typing import Callable

from lights_out import LightsOut
from view_const import PAGE, PAGE_REPLY_BUTTONS, PAGE_COMMANDS


class UserState():

	_hide_message = print
	_show_message = print

	_users_cache = {}

	@classmethod
	def set_hide_message_callback(cls, callback: Callable):
		cls._hide_message = callback

	@classmethod
	def set_show_message_callback(cls, callback: Callable):
		cls._show_message = callback

	@classmethod
	def update_by_command(cls, user_id, message_id, command: str):
		state = cls._get_user_state(user_id)
		page_id = state['page_id']
		if page_id == 'game':
			cls._hide_message(user_id, message_id)
			cls._update_game_view(user_id)

	@classmethod
	def update_by_message(cls, user_id, message_id, message: str):
		state = cls._get_user_state(user_id)
		page_id = state['page_id']

		command = PAGE_REPLY_BUTTONS[page_id].get(message)
		if command is None:
			cls._update_page(user_id, message_id, message)
			return
		state.update(command.content)
		cls._switch_page(user_id, message_id, command.next_page)

	@classmethod
	def update_by_callback(cls, user_id, message_id, data: str):
		state = cls._get_user_state(user_id)
		if message_id != state['last_message_id']:
			return

		page_id = state['page_id']
		if page_id == 'game':
			data = eval(data)
			state['info'] = LightsOut.board_action(user_id, data['row'], data['col'])
			cls._update_game_view(user_id)

	@classmethod
	def _get_user_state(cls, user_id):
		state = cls._users_cache.get(user_id)
		if state is None:
			state = cls._build_user_state(user_id)
			cls._users_cache[user_id] = state
		return state

	@classmethod
	def _build_user_state(cls, user_id):
		state = {}
		state['info'] = info = LightsOut.get_user_info(user_id)
		state['last_message_id'] = -1
		state['page_id'] = PAGE.MAIN
		if info.in_game:
			state['page_id'] = PAGE.GAME
		return state

	@classmethod
	def _switch_page(cls, user_id, message_id, next_page):
		state = cls._get_user_state(user_id)
		actual_page = state['page_id']
		state['page_id'] = next_page
		if next_page is PAGE.NO_PAGE:
			cls._switch_page(user_id, message_id, actual_page)
		elif next_page is PAGE.MAIN:
			cls._switch_page_to_main(user_id, message_id)
		elif next_page is PAGE.INFO:
			cls._switch_page_to_info(user_id, message_id)
		elif next_page is PAGE.HELP:
			cls._switch_page_to_help(user_id, message_id)

	@classmethod
	def _switch_page_to_main(cls, user_id, message_id):
		cls._redisplay_page(user_id)

	@classmethod
	def _switch_page_to_info(cls, user_id, message_id):
		cls._redisplay_page(user_id)

	@classmethod
	def _switch_page_to_help(cls, user_id, message_id):
		cls._redisplay_page(user_id)

	@classmethod
	def _update_page(cls, user_id, message_id, message: str):
		cls._redisplay_page(user_id, inplace=True)

	@classmethod
	def _redisplay_page(cls, user_id, content=None, inplace=False):
		state = cls._get_user_state(user_id)
		state['last_message_id'] = cls._show_message(
			user_id,
			state['last_message_id'],
			inplace,
			state['page_id'],
			content,
		)

