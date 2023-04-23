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
	PAGE.MAIN: [
		'Сейчас Вы в главном меню. Здесь Вы можете подробнее узнать об игре или о нас, команде '
		'разработчиков. Так же Вы можете попробовать сыграть в саму игру.',
	],
	PAGE.INFO: [
		'Данный чат-бот был выполнен двумя талантливыми программистами из Лицея Академии '
		'Яндекс в целях защиты проекта WebServe. Вы можете связаться с нами. Вот наши username '
		'telegram:'
		'\n@av10nyt'
		'\n@name1582222rot3'
	],
	PAGE.HELP: [
		'Lights-out - электронная игра, она содержит поле nxn, каждая клетка которого может быть '
		'в состоянии «включено» или «выключено». Нажатие на любую клетку поля изменит '
		'состояние этой и четырёх соседних клеток. Цель игры — перевести всё поле в состояние'
		' «выключено».'
		'\nПодробнее об игре Вы можете узнать по ссылке:'
		'\nhttps://ru.wikipedia.org/wiki/Lights_Out_(игра)'
		],
	PAGE.CGMD: ['Выберите режим игры.'],
	PAGE.CBRD: ['Выберите размер поля.'],
	PAGE.CLVL: ['Выберите уровень.'],
	PAGE.GAME: ['Удачи!', 'Успехов!', 'Надеюсь, Вы сможете решить эту непростую головомку!'],
}

PAGE_DOCUMENT = {
	PAGE.HELP: 'images/game_rules_image.png',
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
		'4 * 4': PageSwitchCommand(PAGE.GAME, {'width': 4, 'height': 4}),
		'5 * 5': PageSwitchCommand(PAGE.GAME, {'width': 5, 'height': 5}),
		'6 * 6': PageSwitchCommand(PAGE.GAME, {'width': 6, 'height': 6}),
		'7 * 7': PageSwitchCommand(PAGE.GAME, {'width': 7, 'height': 7}),
	},
	PAGE.CLVL: {
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
		'Назад': PageSwitchCommand(PAGE.CGMD),
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
	PAGE.GAME: {
		'quit': PageSwitchCommand(PAGE.GAME, {'quit': True})
	},
}

