"""Время занятий конкретной группы"""

import sys

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


sys.path.append(".")
from db_services.business import get_class_time


async def cmd_class_time(message: types.Message):
    """Время занятий конкретной группы"""
    group_id = int(message.text[10:])
    class_time_text = get_class_time(group_id, is_edit=False)
    await message.answer(class_time_text)


def register_handlers_list_class_time(dp: Dispatcher):
    dp.register_message_handler(cmd_class_time,
                                Text(startswith='/classtime',
                                ignore_case=True),
                                state='*')