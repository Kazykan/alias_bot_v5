"""Добавляем время занятий для группы"""

import sys, re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types


# from common import ikb_start
sys.path.append(".")
from db_services.business import get_groups_list, get_class_time, \
    get_class_rooms_list, add_time, get_one_group, check_class_time_busy, \
    timedelta
from app_bot.handlers.common import ikb_start


class ClassTimeStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по добавлению времени занятий в БД"""
    group_id = State()
    class_room_id = State()
    start_time = State()


async def cb_add_class_time(callback: types.CallbackQuery) -> None:
    """Добавляем время занятий для группы"""
    await callback.message.delete()
    await callback.message.answer(
        f'Введите номер группы просто цифру. Пример: 5\n{get_groups_list(schedule=False)}')
    await ClassTimeStatesGroup.group_id.set()


async def add_classtime_group_id(message: types.Message, state: FSMContext) -> None:
    """Добавляем время занятий для группы этап 2"""
    async with state.proxy() as data:
        data['group_id'] = int(message.text)

    await message.reply(f'{get_class_time(data["group_id"], is_edit=True)} Введите номер кабинета. Пример 1\n'
                        f'{await get_class_rooms_list()}')
    await ClassTimeStatesGroup.next()


async def add_classtime_class_room_id(message: types.Message, state: FSMContext) -> None:
    """Добавляем время занятий для группы этап 3"""
    async with state.proxy() as data:
        data['class_room_id'] = int(message.text)

    await message.reply('Введите время начала занятий в формате день недели цифрой 1-пн, 2-вт, 3-ср, далее 09-00.\n'
                        'Пример: 5 17-30\n')
    await ClassTimeStatesGroup.next()


async def add_classtime_start_time(message: types.Message, state: FSMContext) -> None:
    """Добавляем время занятий для группы - проверка занято ли это время
    в кабинете и личное время преподавателя"""
    try:
        async with state.proxy() as data:
            times = re.split(' |-', message.text)
            data['start_time'] = add_time(hour=int(times[1]), minute=int(times[2]))
            data['isoweekday'] = times[0]
            duration = get_one_group(group_id=data['group_id'])[1]
            data['end_time'] = data['start_time'] + timedelta(minutes=duration)
    except ValueError:
        await message.reply('Не верно введены данные')
    check_class_time_list = check_class_time_busy(start_time=data['start_time'],
                                                  end_time=data['end_time'],
                                                  isoweekday=data['isoweekday'],
                                                  class_room_id=data['class_room_id'],
                                                  group_id=data['group_id'])
    if check_class_time_list[0]:
        await message.reply(check_class_time_list[1])
        await state.finish()
    else:
        await message.reply(check_class_time_list[1])


def register_cb_handlers_add_class_time(dp: Dispatcher):
    dp.register_callback_query_handler(cb_add_class_time,
                                       text_contains='add_class_time',
                                       state='*')  # text_startswith
    dp.register_message_handler(add_classtime_group_id, state=ClassTimeStatesGroup.group_id)
    dp.register_message_handler(add_classtime_class_room_id, state=ClassTimeStatesGroup.class_room_id)
    dp.register_message_handler(add_classtime_start_time, state=ClassTimeStatesGroup.start_time)
    