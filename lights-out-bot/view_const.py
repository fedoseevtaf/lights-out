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
		'Большую часть информации Мы взяли от туда)'
		],
	PAGE.CGMD: ['Выберите тип уровня.'],
	PAGE.CBRD: ['Вы выбрали тип уровня. Теперь выберите размер поля.'],
	PAGE.CLVL: ['Удачи!', 'Успехов!', 'Надеюсь, Вы сможете решить эту непростую головомку!'],
	PAGE.GAME: ['гг',],
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
			{'gmd': 'random'},
		),
		'Готовый уровень': PageSwitchCommand(
			PAGE.CBRD,
			{'gmd': 'level'},
		),
	},
	PAGE.CBRD: {
		'Назад': PageSwitchCommand(PAGE.CGMD),
		'5 * 5': PageSwitchCommand(PAGE.CLVL, {'width': 5, 'height': 5}),
	}, # '6 * 6', '7 * 7', '8 * 8', '9 * 9', '10 * 10'},
	PAGE.CLVL: {
		'Назад': PageSwitchCommand(PAGE.CBRD),
		'This one': PageSwitchCommand(PAGE.GAME, {'level_code': ''}),
	}, # {'1', '2', '3', 'Назад'},
	PAGE.GAME: {}
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
			{'gmd': 'random'},
		),
		'level': PageSwitchCommand(
			PAGE.CBRD,
			{'gmd': 'level'},
		),
	},
	PAGE.CBRD: {
		'back': PageSwitchCommand(PAGE.CGMD),
	},
	PAGE.CLVL: {},
	PAGE.GAME: {},
}

