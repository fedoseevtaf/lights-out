from typing import Callablem, Dict

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

	@classmethod
	def update_by_message(cls, user_id, message_id, message: str):
		state = cls._get_user_state(user_id)
		page_id = state['page_id']
		if page_id == 'game':
			cls._hide_message(user_id, message_id)

	@classmethod
	def update_by_callback(cls, user_id, message_id, data: str):
		state = cls._get_user_state(user_id)
		page_id = state['page_id']
		if page_id == 'game':
			cls._hide_message(user_id, message_id)
			last_message_id = state['info'].last_message_id
			if last_message_id != message_id:
				return

			data = eval(data)
			state['info'] = LightsOut.board_action(data['row'], data['col'])
			content = {
				'board': state['info'].board,
				'width': state['info'].width,
				'height': state['info'].height,
			}
			message_id = cls._show_message(
				user_id,
				state['info'].last_message_id,
				in_place=True,
				page_id,
				content,
			)
			state['info'] = LightsOut.update_message_id(user_id, message_id)

	@classmethod
	def _get_user_state(cls, user_id):
		state = cls._user_cache.get(user_id)
		if state is None:
			state = self._build_user_state(user_id)
			cls._user_cache[user_id] = state
		return state

	@classmethod
	def _build_user_state(cls, user_id):
		state = {}
		state['info'] = info = LightsOut.get_user_info()
		state['page_id'] = 'main'
		if not info.in_game:
			state['page_id'] = 'game'
		return state

