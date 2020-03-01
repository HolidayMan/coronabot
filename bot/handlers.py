import re

from .bot import bot
import bot.phrases as ph
from .keyboards import (MENU_KEYBOARD, deleteKeyboard, BUY_KIT_BUTT0N,
                        CORONAVIRUS_PROTECTION_BUTTON, INF_STATISCTICS_BUTTON, OUR_CHANNEL_BUTTON, BUY_KEYBOARD,
                        BACK_TO_MENU_BUTTON, BUY_BUTTON, CHOOSE_CITY_KEYBOARD, ANOTHER_CITY_BUTTON,
                        BACK_TO_MENU_KEYBOARD)
from .utils import get_statistics, get_current_state, set_state, set_menu_state
from .states import States
from .models import TgUser, Order


@bot.message_handler(func=lambda message: message.text == INF_STATISCTICS_BUTTON.text and get_current_state(message.chat.id) == States.S_CHOOSE_MENU_OPT.value)
def infection_statistics(message):
    return bot.send_message(message.chat.id, get_statistics(), parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == CORONAVIRUS_PROTECTION_BUTTON.text and get_current_state(message.chat.id) == States.S_CHOOSE_MENU_OPT.value)
def coronavirus_protection(message):
    return bot.send_message(message.chat.id, ph.CORONAVIRUS_PROTECTION, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == OUR_CHANNEL_BUTTON.text and get_current_state(message.chat.id) == States.S_CHOOSE_MENU_OPT.value)
def our_channel(message):
    return bot.send_message(message.chat.id, ph.CHANNEL_URL, parse_mode="HTML", reply_markup=MENU_KEYBOARD)


@bot.message_handler(func=lambda message: message.text == BUY_KIT_BUTT0N.text and get_current_state(message.chat.id) == States.S_CHOOSE_MENU_OPT.value)
def buy_kit(message):
    bot.send_message(message.chat.id, ph.BUY_KIT_TEXT, parse_mode="HTML", reply_markup=BUY_KEYBOARD)
    set_state(message.chat.id, States.S_CHOOSE_BUY_MENU.value)


@bot.message_handler(func=lambda message: message.text == BUY_BUTTON.text and get_current_state(message.chat.id) == States.S_CHOOSE_BUY_MENU.value)
def buy(message):
    bot.send_message(message.chat.id, ph.CHOOSE_CITY, parse_mode="HTML", reply_markup=CHOOSE_CITY_KEYBOARD)
    bot.register_next_step_handler(message, handle_city)


def handle_city(message):
    if message.text == BACK_TO_MENU_BUTTON.text:
        return back_to_menu_handler(message)
    elif message.text == ANOTHER_CITY_BUTTON.text:
        bot.send_message(message.chat.id, ph.ENTER_CITY, parse_mode="HTML", reply_markup=CHOOSE_CITY_KEYBOARD)
        bot.register_next_step_handler(message, handle_city)
        return
    else:
        if not message.text:
            bot.register_next_step_handler(message, handle_city)
            return bot.send_message(message.chat.id, ph.INVALID_CITY, parse_mode="HTML", reply_markup=CHOOSE_CITY_KEYBOARD)
        user = TgUser.objects.get(tg_id=message.chat.id)
        new_order = Order(city=message.text, user=user)
        new_order.save()
        bot.send_message(message.chat.id, ph.ENTER_ADDRESS, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
        bot.register_next_step_handler(message, handle_address)


def handle_address(message):
    if message.text == BACK_TO_MENU_BUTTON.text:
        user = TgUser.objects.get(tg_id=message.chat.id)
        order = Order.objects.filter(user=user).order_by("-id")[0]
        order.delete()
        return back_to_menu_handler(message)
    else:
        if not message.text:
            bot.register_next_step_handler(message, handle_address)
            return bot.send_message(message.chat.id, ph.INVALID_ADDRESS, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
        user = TgUser.objects.get(tg_id=message.chat.id)
        order = Order.objects.filter(user=user).order_by("-id")[0]
        order.address = message.text
        order.save()
        bot.send_message(message.chat.id, ph.ENTER_PHONE, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
        bot.register_next_step_handler(message, handle_phone)


def handle_phone(message):
    if message.text == BACK_TO_MENU_BUTTON.text:
        user = TgUser.objects.get(tg_id=message.chat.id)
        order = Order.objects.filter(user=user).order_by("-id")[0]
        order.delete()
        return back_to_menu_handler(message)
    if not message.text:
        bot.register_next_step_handler(message, handle_phone)
        return bot.send_message(message.chat.id, ph.INVALID_PHONE, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
    phone_pattern = r"(\+)*(7|){0,1}([0-9]){7,11}$"
    if not re.match(phone_pattern, message.text):
        bot.register_next_step_handler(message, handle_phone)
        return bot.send_message(message.chat.id, ph.INVALID_PHONE, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
    else:
        user = TgUser.objects.get(tg_id=message.chat.id)
        order = Order.objects.filter(user=user).order_by("-id")[0]
        order.phone = message.text
        order.save()
        bot.send_message(message.chat.id, ph.ENTER_AMOUNT, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
        bot.register_next_step_handler(message, handle_amount)


def handle_amount(message):
    if message.text == BACK_TO_MENU_BUTTON.text:
        user = TgUser.objects.get(tg_id=message.chat.id)
        order = Order.objects.filter(user=user).order_by("-id")[0]
        order.delete()
        return back_to_menu_handler(message)
    if not message.text:
        bot.register_next_step_handler(message, handle_amount)
        return bot.send_message(message.chat.id, ph.INVALID_AMOUNT, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)
    try:
        amount = int(message.text)
        if not 0 < amount <= 10:
            raise ValueError
    except ValueError:
        return bot.send_message(message.chat.id, ph.INVALID_AMOUNT, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)

    user = TgUser.objects.get(tg_id=message.chat.id)
    order = Order.objects.filter(user=user).order_by("-id")[0]
    order.amount = amount
    order.save()
    bot.send_message(message.chat.id, ph.ORDER_ADDED, parse_mode="HTML", reply_markup=MENU_KEYBOARD)
    set_menu_state(message.chat.id)
    send_order_to_owners(order)


def build_order_message(order):
    return ph.ORDER_MESSAGE % (order.user.username,
                               order.phone,
                               order.city,
                               order.address,
                               order.amount,
                               order.date_added.strftime("%A %d.%m.%Y %H:%M UTC+0"))


def send_order_to_owners(order):
    owners = TgUser.objects.filter(send_orders=True)
    message_text = build_order_message(order)
    for owner in owners:
        bot.send_message(owner.tg_id, message_text, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == BACK_TO_MENU_BUTTON.text)
def back_to_menu_handler(message):
    set_menu_state(message.chat.id)
    return bot.send_message(message.chat.id, ph.MENU, reply_markup=MENU_KEYBOARD)
