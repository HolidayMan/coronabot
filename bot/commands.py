from .bot import bot
from .utils import user_exists, set_menu_state
from .models import TgUser
import bot.phrases as ph
from .keyboards import MENU_KEYBOARD


@bot.message_handler(commands=['start'])
def cmd_start(message):
    if not user_exists(message):
        new_user = TgUser(tg_id=message.chat.id)
        if message.chat.username:
            new_user.username = message.chat.username
        if message.chat.first_name:
            new_user.first_name = message.chat.first_name
        new_user.save()

    bot.send_message(message.chat.id, ph.START_TEXT, parse_mode="HTML", reply_markup=MENU_KEYBOARD)
    bot.send_video(message.chat.id, ph.START_VIDEO_ID)

    set_menu_state(message.chat.id)
