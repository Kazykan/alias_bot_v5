"""Добавляем новую группу"""
"""++++ добавить опросник онлайн или офлайн группа +++++"""

import sys

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types


# from common import ikb_start
sys.path.append(".")
from db_services.business import create_new_group, get_teacher_list
from app_bot.handlers.common import ikb_start


class GroupStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по добавлению Группы в БД"""
    name = State()
    quota = State()
    price = State()
    duration = State()
    description = State()
    grade = State()
    teacher_id = State()


async def cb_add_new_group(callback: types.CallbackQuery, state: FSMContext):
    """Добавляем новую группу"""
    await callback.message.delete()
    await callback.message.answer('Напиши название группы!')
    await GroupStatesGroup.name.set()


async def handle_group_name(message: types.Message, state: FSMContext):
    """Добавляем новую группу - 2 пункт"""
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Кол-во учеников в группе. Пример: 6')
    await GroupStatesGroup.next()


async def handle_group_quota(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 3 пункт"""
    async with state.proxy() as data:
        data['quota'] = int(message.text)
    await message.reply('Стоимость занятия просто цифры без р. Пример: 650')
    await GroupStatesGroup.next()


async def handle_group_price(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 4 пункт"""
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await message.reply('Длительность занятия просто цифра в минутах. Пример: 60')
    await GroupStatesGroup.next()


async def handle_group_duration(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 5 пункт"""
    async with state.proxy() as data:
        data['duration'] = int(message.text)
    await message.reply('Описание. Пример: -')
    await GroupStatesGroup.next()


async def handle_group_description(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 6 пункт"""
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply('Какие школ. классы занимаются, цифры через пробел. Пример: 1 2 3')
    await GroupStatesGroup.next()


async def handle_group_grade(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 7 пункт"""
    try:
        async with state.proxy() as data:
            data['grade'] = [int(i) for i in message.text.split()]  # Разделяем и преобразуем в цифры
        await message.reply(f'Кто ведет эту группу введите цифру препод.\n{get_teacher_list(schedule=2)}\n Пример: 1')
        await GroupStatesGroup.next()
    except ValueError:
        await message.reply('Не верно введены данные\n'
        'Какие школ. классы занимаются, цифры через пробел. Пример: 1 2 3')


async def handle_group_teacher_id(message: types.Message, state: FSMContext) -> None:
    """После ответа на последний вопрос создаем группу в БД и выводим ответ"""
    async with state.proxy() as data:
        data['teacher_id'] = int(message.text)
    create_new_group(name=data['name'], quota=data['quota'],
                     price=data['price'], duration=data['duration'],
                     description=data['description'], grades=data['grade'],
                     teacher_id=data['teacher_id'])

    await message.reply('Спасибо группа создана', reply_markup=ikb_start())
    await state.finish()


def register_cb_handlers_add_new_group(dp: Dispatcher):
    dp.register_callback_query_handler(cb_add_new_group,
                                       text_contains='add_new_group',
                                       state='*')  # text_startswith
    dp.register_message_handler(handle_group_name, state=GroupStatesGroup.name)
    dp.register_message_handler(handle_group_quota, state=GroupStatesGroup.quota)
    dp.register_message_handler(handle_group_price, state=GroupStatesGroup.price)
    dp.register_message_handler(handle_group_duration, state=GroupStatesGroup.duration)
    dp.register_message_handler(handle_group_description, state=GroupStatesGroup.description)
    dp.register_message_handler(handle_group_grade, state=GroupStatesGroup.grade)
    dp.register_message_handler(handle_group_teacher_id, state=GroupStatesGroup.teacher_id)
