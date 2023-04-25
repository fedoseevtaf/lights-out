import json
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
	def update_by_command(cls, user_id, message_id, command_text: str):
		state = cls._get_user_state(user_id)
		page_id = state['page_id']

		command = PAGE_COMMANDS[page_id].get(command_text)
		if command is None:
			cls._update_page(user_id, message_id, command_text)
			return
		state.update(command.content)
		cls._switch_page(user_id, message_id, command.next_page)

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
		if state['page_id'] == PAGE.GAME:
			cls._click_at_page_game(user_id, message_id, data)

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
	def _click_at_page_game(cls, user_id, message_id, data):
		state = cls._get_user_state(user_id) # noqa
		if data == 'quit':
			return cls._quit_game(user_id, message_id)
		data = json.loads(data)
		is_win = LightsOut.board_action(user_id, **data)
		cls._update_game_page_view(user_id)
		if is_win:
			cls._quit_game(user_id, message_id)

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
		elif next_page is PAGE.CGMD:
			cls._switch_page_to_cgmd(user_id, message_id)
		elif next_page is PAGE.CBRD:
			cls._switch_page_to_cbrd(user_id, message_id)
		elif next_page is PAGE.CLVL:
			cls._switch_page_to_clvl(user_id, message_id)
		elif next_page is PAGE.GAME:
			cls._switch_page_to_game(user_id, message_id)

	@classmethod
	def _switch_page_to_main(cls, user_id, message_id):
		cls._display_page(user_id)

	@classmethod
	def _switch_page_to_info(cls, user_id, message_id):
		cls._display_page(user_id)

	@classmethod
	def _switch_page_to_help(cls, user_id, message_id):
		cls._display_page(user_id)

	@classmethod
	def _switch_page_to_cgmd(cls, user_id, message_id):
		cls._display_page(user_id)

	@classmethod
	def _switch_page_to_cbrd(cls, user_id, message_id):
		cls._display_page(user_id)

	@classmethod
	def _switch_page_to_clvl(cls, user_id, message_id):
		cls._display_page(user_id)

	@classmethod
	def _switch_page_to_game(cls, user_id, message_id):
		state = cls._get_user_state(user_id)
		if 'quit' in state:
			del state['quit']
			return cls._quit_game(user_id, message_id)
		game_mode = state.get('gmd')
		width = state.get('width')
		height = state.get('height')
		lvl_code = state.get('level_code')
		LightsOut.start_game(user_id, game_mode, width, height, lvl_code)
		state['info'] = LightsOut.get_user_info(user_id)
		if not state['info'].in_game:
			return cls._switch_page(user_id, message_id, PAGE.MAIN)
		cls._update_game_page_view(user_id, False)

	@classmethod
	def _quit_game(cls, user_id, message_id):
		state = cls._get_user_state(user_id)
		LightsOut.quit_game(user_id)
		state['info'] = LightsOut.get_user_info(user_id)
		if not state['info'].in_game:
			return cls._switch_page(user_id, message_id, PAGE.MAIN)
		cls._update_game_page_view(user_id, False)

	@classmethod
	def _update_game_page_view(cls, user_id, in_place: bool = True):
		state = cls._get_user_state(user_id)
		info = state['info'] = LightsOut.get_user_info(user_id)
		content = {'width': info.width, 'height': info.height, 'board': info.board}
		cls._display_page(user_id, content, in_place, only_markup=True)

	@classmethod
	def _update_page(cls, user_id, message_id, message: str):
		state = cls._get_user_state(user_id)
		page = state['page_id']
		if page is PAGE.MAIN:
			cls._update_by_message_page_main(user_id, message_id, message)
		elif page is PAGE.INFO:
			cls._update_by_message_page_info(user_id, message_id, message)
		elif page is PAGE.HELP:
			cls._update_by_message_page_help(user_id, message_id, message)
		elif page is PAGE.CGMD:
			cls._update_by_message_page_cgmd(user_id, message_id, message)
		elif page is PAGE.CBRD:
			cls._update_by_message_page_cbrd(user_id, message_id, message)
		elif page is PAGE.CLVL:
			cls._update_by_message_page_clvl(user_id, message_id, message)
		elif page == PAGE.GAME:
			cls._update_by_message_page_game(user_id, message_id, message)

	@classmethod
	def _update_by_message_page_main(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._display_page(user_id, in_place=True)

	@classmethod
	def _update_by_message_page_help(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._display_page(user_id, in_place=True)

	@classmethod
	def _update_by_message_page_info(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._display_page(user_id, in_place=True)

	@classmethod
	def _update_by_message_page_cgmd(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._display_page(user_id, in_place=True)

	@classmethod
	def _update_by_message_page_cbrd(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._display_page(user_id, in_place=True)

	@classmethod
	def _update_by_message_page_clvl(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._display_page(user_id, in_place=True)

	@classmethod
	def _update_by_message_page_game(cls, user_id, message_id, message):
		cls._hide_message(user_id, message_id)
		cls._update_game_page_view(user_id)

	@classmethod
	def _display_page(
			cls, user_id, content=None,
			in_place=False, only_markup: bool = False,
		):
		state = cls._get_user_state(user_id)
		state['last_message_id'] = cls._show_message(
			user_id,
			state['last_message_id'],
			in_place,
			state['page_id'],
			content,
			only_markup,
		)

