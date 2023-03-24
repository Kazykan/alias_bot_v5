"""Добавляем новую группу"""
"""++++ добавить опросник онлайн или офлайн группа +++++"""

import sys

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types

sys.path.append(".")
from db_services.business import get_groups_list, add_date, create_new_user
from app_bot.handlers.common import ikb_start



class UserStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по добавлению ученика
    в БД"""
    first_name = State()
    last_name = State()
    town = State()
    description = State()
    birthday = State()
    phone_number = State()
    group_id = State()


async def cb_add_new_user(callback: types.CallbackQuery) -> None:
    """Добавляем нового ученика"""
    await callback.message.delete()
    await callback.message.answer('Напишите имя ученика!')
    await UserStatesGroup.first_name.set()


async def add_new_user_first_name(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика пункт 2"""
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.reply('Напишите фамилие ученика')
    await UserStatesGroup.next()


async def add_new_user_last_name(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика пункт 3"""
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.reply('Напишите город')
    await UserStatesGroup.next()


async def add_new_user_town(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика пункт 4"""
    async with state.proxy() as data:
        data['town'] = message.text
    await message.reply('Описание, ФИО родителей, ном. тел. родителей и прочее в произвольной форме')
    await UserStatesGroup.next()


async def add_new_user_description(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика пункт 5"""
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply('День рождения в формате 25.11.1998')
    await UserStatesGroup.next()


async def add_new_user_birthday(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика пункт 6"""
    async with state.proxy() as data:
        data['birthday'] = add_date(message.text)
    await message.reply('Номер телефона в формате 8 962 412 50 81')
    await UserStatesGroup.next()


async def add_new_user_phone_number(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика пункт 7"""
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.reply(f'Выберите группу из списка. Напишите номер группы. Пример: 2\n'
                        f'{get_groups_list(schedule=False)}')
    await UserStatesGroup.next()


async def add_new_user_group_id(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика - запускаем проверку и добавляем ученика"""
    async with state.proxy() as data:
        data['group_id'] = message.text
    create_new_user(first_name=data['first_name'], last_name=data['last_name'],
                    town=data['town'], description=data['description'], birthday=data['birthday'],
                    phone_number=data['phone_number'], group_id=data['group_id'], is_active=True)

    await message.reply('Спасибо пользователь создан', reply_markup=ikb_start())
    await state.finish()


def register_cb_handlers_add_new_user(dp: Dispatcher):
    dp.register_callback_query_handler(cb_add_new_user,
                                       text_contains='add_new_user',
                                       state='*')  # text_startswith
    dp.register_message_handler(add_new_user_first_name, state=UserStatesGroup.first_name)
    dp.register_message_handler(add_new_user_last_name, state=UserStatesGroup.last_name)
    dp.register_message_handler(add_new_user_town, state=UserStatesGroup.town)
    dp.register_message_handler(add_new_user_description, state=UserStatesGroup.description)
    dp.register_message_handler(add_new_user_birthday, state=UserStatesGroup.birthday)
    dp.register_message_handler(add_new_user_phone_number, state=UserStatesGroup.phone_number)
    dp.register_message_handler(add_new_user_group_id, state=UserStatesGroup.group_id)
