from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Добро пожаловать!',
        reply_markup=ikb_start()
    )


async def cb_start(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(
        'Добро пожаловать!',
        reply_markup=ikb_start()
        )


def ikb_start() -> types.InlineKeyboardMarkup:
    """Кнопки первые: Записаться, ученику, учителю"""
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Записаться в группу 🇬🇧', callback_data='reservation')],
        [types.InlineKeyboardButton(text='Ученику расписание 🗓', callback_data='group_schedule')],
        [types.InlineKeyboardButton(text='Учителю 👨‍🏫', callback_data='edit')],
    ], reply_markup=types.ReplyKeyboardRemove())
    return ikb


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Action canceled',
                         reply_markup=ikb_start())


async def secret_command(message: types.Message):
    await message.answer(
        'Congratulations! This command is available only to the bot administrator')


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_cancel,
                                Text(equals='отмена',
                                ignore_case=True),
                                state='*')
    dp.register_callback_query_handler(cb_start, text_contains='start', state='*')
    dp.register_message_handler(secret_command,
                                IDFilter(user_id=admin_id),
                                commands='abracadabra')
