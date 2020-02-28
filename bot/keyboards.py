from telebot import types

deleteKeyboard = types.ReplyKeyboardRemove()

INF_STATISCTICS_BUTTON = types.KeyboardButton("Статистика заражений")
CORONAVIRUS_PROTECTION_BUTTON = types.KeyboardButton("Меры защиты от коронавируса")
BUY_KIT_BUTT0N = types.KeyboardButton("Купить набор со скидкой 20%")
OUR_CHANNEL_BUTTON = types.KeyboardButton("Наш канал")
BUY_BUTTON = types.KeyboardButton("Купить")
BACK_TO_MENU_BUTTON = types.KeyboardButton("Назад")

MOSCOW_BUTTON = types.KeyboardButton("Москва")
MO_BUTTON = types.KeyboardButton("МО")
ANOTHER_CITY_BUTTON = types.KeyboardButton("Другой город")

MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=False)
MENU_KEYBOARD.add(INF_STATISCTICS_BUTTON, CORONAVIRUS_PROTECTION_BUTTON, BUY_KIT_BUTT0N, OUR_CHANNEL_BUTTON)

BUY_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
BUY_KEYBOARD.add(BUY_BUTTON, BACK_TO_MENU_BUTTON)

CHOOSE_CITY_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
CHOOSE_CITY_KEYBOARD.add(MOSCOW_BUTTON, MO_BUTTON, ANOTHER_CITY_BUTTON)
CHOOSE_CITY_KEYBOARD.row(BACK_TO_MENU_BUTTON)

BACK_TO_MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
BACK_TO_MENU_KEYBOARD.add(BACK_TO_MENU_BUTTON)
