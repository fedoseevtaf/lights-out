from typing import Callable

from lights_out import LightsOut


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
		if page_id == 'game':
			cls._hide_message(user_id, message_id)
			cls._update_game_view(user_id)

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
	def _update_game_view(cls, user_id, *, first_view_update: bool = False):
			state = cls._get_user_state(user_id)
			page_id = state['page_id']
			last_message_id = state['last_message_id']
			info = state['info']
			content = {
				'board': info.board,
				'width': info.width,
				'height': info.height,
			}
			state['last_message_id'] = cls._show_message(
				user_id,
				last_message_id,
				not first_view_update,
				page_id,
				content,
			)

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
		state['page_id'] = 'main'
		if info.in_game:
			state['page_id'] = 'game'
		return state

