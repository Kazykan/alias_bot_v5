"""Время занятий конкретного преподавателя"""

import sys

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


sys.path.append(".")
from db_services.business import get_schedule_teacher


async def cmd_schedule_teachers(message: types.Message):
    """Время занятий конкретного преподавателя"""
    teacher_name = int(message.text[9:])
    schedule_teacher_text = get_schedule_teacher(teacher_name)
    await message.answer(schedule_teacher_text)


def register_handlers_schedule_teachers(dp: Dispatcher):
    dp.register_message_handler(cmd_schedule_teachers,
                                Text(startswith='/schedule',
                                ignore_case=True),
                                state='*')