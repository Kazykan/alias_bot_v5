"""Отработка кнопки Добавить|удалить|поправить группу"""

from aiogram import Dispatcher, types


async def cb_tasks_class_time(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить время занятий"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=get_tasks_class_time_ikb())



def get_tasks_class_time_ikb() -> types.InlineKeyboardMarkup:
    """Кнопки редактирования ученика, Добавить|удалить|поправить ученика"""
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Добавить время занятий', callback_data='add_class_time')],
        [types.InlineKeyboardButton('Удалить время занятий', callback_data='remove_class_time')],
        [types.InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=types.ReplyKeyboardRemove())
    return ikb


def register_cb_handlers_tasks_class_time(dp: Dispatcher):
    dp.register_callback_query_handler(
        cb_tasks_class_time,
        text_contains='tasks_class_time',
        state='*')  # text_startswith