"""Отработка кнопки Добавить|удалить кабинет"""

from aiogram import Dispatcher, types


async def cb_tasks_class_room(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить время занятий"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=ikb_tasks_class_time())


def ikb_tasks_class_time() -> types.InlineKeyboardMarkup:
    """Кнопки Добавить|удалить кабинет"""
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Добавить кабинет', callback_data='add_class_room')],
        [types.InlineKeyboardButton('Удалить кабинет', callback_data='remove_class_room')],
        [types.InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=types.ReplyKeyboardRemove())
    return ikb


def register_cb_handlers_tasks_class_room(dp: Dispatcher):
    dp.register_callback_query_handler(
        cb_tasks_class_room,
        text_contains='tasks_class_room',
        state='*')  # text_startswith
