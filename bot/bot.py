import telebot
import logging
from coronabot.settings import TOKEN

bot = telebot.TeleBot(TOKEN)

logger = telebot.logger
logging.basicConfig(filename='bot.log', filemode='a', format='%(asctime)s:%(name)s - %(message)s')

bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
