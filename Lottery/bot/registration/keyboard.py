from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_check_subscribe_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscribe")
    )
    return keyboard.as_markup()

def get_sex_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="👨 Мужской", callback_data="sex_male"),
        InlineKeyboardButton(text="👩 Женский", callback_data="sex_female")
    )
    return keyboard.adjust(2).as_markup()

