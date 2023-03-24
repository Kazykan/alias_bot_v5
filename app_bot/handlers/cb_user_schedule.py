import sys

from aiogram import Dispatcher, types

sys.path.append(".")
from db_services.business import get_groups_list


async def cb_group_schedule(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(get_groups_list(schedule=True))
    

def register_cb_handlers_group_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(cb_group_schedule,
                                       text_contains='group_schedule',
                                       state='*')  # text_startswith