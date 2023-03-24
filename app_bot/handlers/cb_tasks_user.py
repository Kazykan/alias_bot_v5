"""Отработка кнопки Добавить|удалить|поправить группу"""

from aiogram import Dispatcher, types


async def cb_tasks_user(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить|поправить ученика"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=ikb_tasks_user())



def ikb_tasks_user() -> types.InlineKeyboardMarkup:
    """Кнопки редактирования ученика, Добавить|удалить|поправить ученика"""
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Добавить ученика', callback_data='add_new_user')],
        [types.InlineKeyboardButton('Удалить ученика', callback_data='remove_user')],
        [types.InlineKeyboardButton('Поправить данные ученика', callback_data='fix_user')],
        [types.InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=types.ReplyKeyboardRemove())
    return ikb


def register_cb_handlers_tasks_user(dp: Dispatcher):
    dp.register_callback_query_handler(cb_tasks_user,
                                       text_contains='tasks_user',
                                       state='*')  # text_startswith