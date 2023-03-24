from aiogram import Dispatcher, types


async def cmd_edit(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=ikb_edit_all_data())


def ikb_edit_all_data() -> types.InlineKeyboardMarkup:
    """Кнопки редактирования данных, добавить еще кнопки ++++"""
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Доб.|удалить|поправить группу 🎩',
                                    callback_data='tasks_group')],
        [types.InlineKeyboardButton('Доб.|удалить|поправить ученика 🤖',
                                    callback_data='tasks_user')],
        [types.InlineKeyboardButton('Доб.|удалить время занятий ⌚',
                                    callback_data='tasks_class_time')],
        [types.InlineKeyboardButton('Доб.|удалить кабинет 🚪',
                                    callback_data='tasks_class_room')],
        [types.InlineKeyboardButton('Расписания учителей 🎓',
                                    callback_data='teacher_schedule')],
        [types.InlineKeyboardButton('Назад', callback_data='start')],
    ], reply_markup=types.ReplyKeyboardRemove())
    return ikb


def register_cb_handlers_edit(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_edit,
                                       text_contains='edit',
                                       state='*')  # text_startswith