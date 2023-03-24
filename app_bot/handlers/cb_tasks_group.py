"""Отработка кнопки Добавить|удалить|поправить группу"""

from aiogram import Dispatcher, types


async def cb_tasks_group(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить|поправить группу"""
    await callback.message.delete()
    await callback.message.answer('Редактирование данных:',
                                  reply_markup=ikb_tasks_group())


def ikb_tasks_group() -> types.InlineKeyboardMarkup:
    """Кнопки редактирования группы, Добавить|удалить|поправить группу"""
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Добавить группу', callback_data='add_new_group')],
        [types.InlineKeyboardButton('Удалить группу', callback_data='remove_group')],
        [types.InlineKeyboardButton('Поправить данные группы', callback_data='fix_group')],
        [types.InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=types.ReplyKeyboardRemove())
    return ikb


def register_cb_handlers_tasks_group(dp: Dispatcher):
    dp.register_callback_query_handler(cb_tasks_group,
                                       text_contains='tasks_group',
                                       state='*')  # text_startswith