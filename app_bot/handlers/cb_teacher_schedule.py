import sys

from aiogram import Dispatcher, types

sys.path.append(".")
from db_services.business import get_teacher_list


async def cb_teacher_schedule(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(get_teacher_list(schedule=1))


def register_cb_handlers_teacher_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(cb_teacher_schedule,
                                       text_contains='teacher_schedule',
                                       state='*')