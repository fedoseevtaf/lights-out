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
	PAGE.MAIN: 'Hi there, I am Бот. Трофим надо придумать приветствующие сообщение!',
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
		#'Играть': PageSwitchCommand(PAGE.CGMD),
		'Об игре': PageSwitchCommand(PAGE.HELP),
	},
	PAGE.INFO: {
		'Назад': PageSwitchCommand(PAGE.MAIN),
	},
	PAGE.HELP: {
		'Назад': PageSwitchCommand(PAGE.MAIN)
	}
	#PAGE.CGMD: {'Назад', 'Сгенерированная', 'Готовая'},
	#PAGE.CBRD: {'5 * 5', '6 * 6', '7 * 7', '8 * 8', '9 * 9', '10 * 10', 'Назад'},
	#PAGE.CLVL: {'1', '2', '3', 'Назад'},
	#PAGE.GAME: {'Назад', 'Стоп'}
}

PAGE_COMMANDS = {
}

