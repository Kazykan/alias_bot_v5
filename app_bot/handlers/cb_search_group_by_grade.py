"""Поиск групп по классам для записи на тестирование"""

import sys

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

sys.path.append(".")
from db_services.business import get_groups_reservation_text

class GradeSearchStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по поиску группы по классу ученика
    и запись на тестирование"""
    grade_name = State()
    group_id = State()
    contact_info = State()

async def cb_search_group_by_grade(callback: types.CallbackQuery) -> None:
    """Поиск групп по классам для записи на тестирование"""
    await callback.message.delete()
    await callback.message.answer(
        'Напишите класс в котором учитесь вы или ваш ребенок, 0 - дошкольник, 12 - студент, 13 - взрослый',)
    await GradeSearchStatesGroup.grade_name.set()


async def cb_search_group_by_grade_grade_name(message: types.Message, state: FSMContext) -> None:
    """Поиск групп по классам для записи на тестирование"""
    async with state.proxy() as data:
        data['grade_name'] = int(message.text)
    group_list = get_groups_reservation_text(grade_number=data['grade_name'])
    await message.reply(f'Напишите номер группы который вам подходит по расписанию: \n{group_list}')
    await GradeSearchStatesGroup.group_id.set()


async def cb_search_group_by_grade_group_id(message: types.Message, state: FSMContext) -> None:
    """Поиск групп по классам для записи на тестирование"""
    async with state.proxy() as data:
        data['group_id'] = (message.text)
    await message.reply('Напишите номер телефона для связи и ваше имя:\n')
    await GradeSearchStatesGroup.contact_info.set()


async def cb_search_group_by_grade_contact_info(message: types.Message, state: FSMContext) -> None:
    """Поиск групп по классам для записи на тестирование"""
    async with state.proxy() as data:
        data['contact_info'] = (message.text)
    await message.reply('Большое спасибо, мы обязательно с вами свяжемся')
    text_reservation = get_groups_reservation_text(grade_number=data['grade_name'])
    text_reservation += f"\n\ncontact - {data['contact_info']}\n group: {data['group_id']}. grade - {data['grade_name']}"
    await send_message_chanel(text_reservation)
    await state.finish()


async def send_message_chanel(text: str):
    """Отправка сообщения в канал"""
    # await bot.send_message(CHANNEL_ID, text)
    pass


def register_cb_handlers_search_group_by_grade(dp: Dispatcher):
    dp.register_callback_query_handler(
        cb_search_group_by_grade,
        text_contains='reservation',
        state='*')  # text_startswith
    dp.register_message_handler(
        cb_search_group_by_grade_grade_name,
        state=GradeSearchStatesGroup.grade_name)
    dp.register_message_handler(
        cb_search_group_by_grade_group_id,
        state=GradeSearchStatesGroup.group_id)
    dp.register_message_handler(
        cb_search_group_by_grade_contact_info,
        state=GradeSearchStatesGroup.contact_info)
