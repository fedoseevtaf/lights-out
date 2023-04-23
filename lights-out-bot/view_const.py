from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


@dataclass
class PageSwitchCommand():
	next_page: Enum
	content: Dict = field(default_factory=dict)


PAGE = Enum('PAGE', (
	'MAIN',
	'INFO',
	'HELP',
	'CGMD',
	'CLVL',
	'CBRD',
	'GAME',

	'NO_PAGE',
))


PAGE_TEXT = {
	PAGE.MAIN: (
		'Hi there, I am Бот. Трофим надо придумать'
		'приветствующие сообщение!'
	),
	PAGE.INFO: 'О нас... Пока ничего',
	PAGE.HELP: 'ПОМОГИТЕ!!! ТРОФИМ ДЕРЖИТ МЕНЯ В ЗАЛОЖНИКАХ',
	PAGE.CGMD: 'Выберите тип доски',
	PAGE.CBRD: 'Выберите размер доски',
	PAGE.CLVL: 'Выберите уровень',
	PAGE.GAME: 'Удачный игры'
}

PAGE_REPLY_BUTTONS = {
	PAGE.MAIN: {
		'О нас': PageSwitchCommand(PAGE.INFO),
		'Играть': PageSwitchCommand(PAGE.CGMD),
		'Об игре': PageSwitchCommand(PAGE.HELP),
	},
	PAGE.INFO: {
		'Назад': PageSwitchCommand(PAGE.MAIN),
	},
	PAGE.HELP: {
		'Назад': PageSwitchCommand(PAGE.MAIN)
	},
	PAGE.CGMD: {
		'Назад': PageSwitchCommand(PAGE.MAIN),
		'Случайный уровень': PageSwitchCommand(
			PAGE.CBRD,
			{'gmd': 'random', 'level_code': ''},
		),
		'Готовый уровень': PageSwitchCommand(
			PAGE.CLVL,
			{'gmd': 'level', 'width': 5, 'height': 5},
		),
	},
	PAGE.CBRD: {
		'Назад': PageSwitchCommand(PAGE.CGMD),
		'3 * 3': PageSwitchCommand(PAGE.GAME, {'width': 3, 'height': 3}),
		'4 * 4': PageSwitchCommand(PAGE.GAME, {'width': 3, 'height': 4}),
		'5 * 5': PageSwitchCommand(PAGE.GAME, {'width': 5, 'height': 5}),
		'6 * 6': PageSwitchCommand(PAGE.GAME, {'width': 6, 'height': 6}),
		'7 * 7': PageSwitchCommand(PAGE.GAME, {'width': 7, 'height': 7}),
	},
	PAGE.CLVL: {
		'Назад': PageSwitchCommand(PAGE.CGMD),
		'1': PageSwitchCommand(PAGE.GAME, {'level_code': '1'}),
		'2': PageSwitchCommand(PAGE.GAME, {'level_code': '2'}),
		'3': PageSwitchCommand(PAGE.GAME, {'level_code': '3'}),
		'4': PageSwitchCommand(PAGE.GAME, {'level_code': '4'}),
		'5': PageSwitchCommand(PAGE.GAME, {'level_code': '5'}),
		'6': PageSwitchCommand(PAGE.GAME, {'level_code': '6'}),
		'7': PageSwitchCommand(PAGE.GAME, {'level_code': '7'}),
		'8': PageSwitchCommand(PAGE.GAME, {'level_code': '8'}),
		'9': PageSwitchCommand(PAGE.GAME, {'level_code': '9'}),
		'10': PageSwitchCommand(PAGE.GAME, {'level_code': '10'}),
		'11': PageSwitchCommand(PAGE.GAME, {'level_code': '11'}),
		'12': PageSwitchCommand(PAGE.GAME, {'level_code': '12'}),
		'13': PageSwitchCommand(PAGE.GAME, {'level_code': '13'}),
		'14': PageSwitchCommand(PAGE.GAME, {'level_code': '14'}),
		'15': PageSwitchCommand(PAGE.GAME, {'level_code': '15'}),
	},
	PAGE.GAME: {},
}

PAGE_COMMANDS = {
	PAGE.MAIN: {
		'about': PageSwitchCommand(PAGE.INFO),
		'help': PageSwitchCommand(PAGE.HELP),
		'play': PageSwitchCommand(PAGE.CGMD),
	},
	PAGE.INFO: {
		'back': PageSwitchCommand(PAGE.MAIN),
	},
	PAGE.HELP: {
		'back': PageSwitchCommand(PAGE.MAIN),
	},
	PAGE.CGMD: {
		'back': PageSwitchCommand(PAGE.MAIN),
		'random': PageSwitchCommand(
			PAGE.CBRD,
			{'gmd': 'random', 'level_code': ''},
		),
		'level': PageSwitchCommand(
			PAGE.CBRD,
			{'gmd': 'level', 'width': 5, 'height': 5},
		),
	},
	PAGE.CBRD: {
		'back': PageSwitchCommand(PAGE.CGMD),
	},
	PAGE.CLVL: {
		'back': PageSwitchCommand(PAGE.CGMD),
	},
	PAGE.GAME: {},
}

