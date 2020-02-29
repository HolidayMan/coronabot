from vedis import Vedis

from .bot import bot
from .models import TgUser
from coronabot.settings import STATISTICS_TEXT_FILE, STATES_FILE
from .parser import build_tg_message
from .states import States


def user_exists(message) -> bool:
    return TgUser.objects.filter(tg_id=message.chat.id).exists()


def get_statistics() -> str:
    with open(STATISTICS_TEXT_FILE) as f:
        return f.read()


def set_state(user_id, value):
    with Vedis(STATES_FILE) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_current_state(user_id):
    with Vedis(STATES_FILE) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return States.S_CHOOSE_MENU_OPT.value


def set_menu_state(user_id):
    with Vedis(STATES_FILE) as db:
        try:
            db[user_id] = States.S_CHOOSE_MENU_OPT.value
            return True
        except:
            return False


def parse_statistics():
    try:
        message = build_tg_message()
        with open(STATISTICS_TEXT_FILE, "w") as f:
            f.write(message)
    except:
        while True:
            try:
                message = build_tg_message()
                f.write(message)
                break
            except:
                continue


def send_statistics():
    users = TgUser.objects.all()
    statistics = get_statistics()
    for user in users:
        try:
            bot.send_message(user.tg_id, statistics, parse_mode="HTML")
        except:
            continue
