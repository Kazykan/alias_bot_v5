import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app_bot.handlers.cb_add_class_time import register_cb_handlers_add_class_time
from app_bot.handlers.cb_tasks_class_room import register_cb_handlers_tasks_class_room
from app_bot.handlers.cb_tasks_user import register_cb_handlers_tasks_user
from app_bot.handlers.common import register_handlers_common
from app_bot.config_reader import load_config
from app_bot.handlers.cb_add_new_group import register_cb_handlers_add_new_group
from app_bot.handlers.cb_search_group_by_grade import register_cb_handlers_search_group_by_grade
from app_bot.handlers.cb_tasks_class_time import register_cb_handlers_tasks_class_time
from app_bot.handlers.cb_tasks_group import register_cb_handlers_tasks_group
from app_bot.handlers.cb_teacher_schedule import register_cb_handlers_teacher_schedule
from app_bot.handlers.cmd_class_time import register_handlers_list_class_time
from app_bot.handlers.cb_edit import register_cb_handlers_edit
from app_bot.handlers.cb_user_schedule import register_cb_handlers_group_schedule
from app_bot.handlers.cmd_schedule_teachers import register_handlers_schedule_teachers
from app_bot.handlers.cb_add_new_user import register_cb_handlers_add_new_user



logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начать общение'),
        BotCommand(command='/food', description='Заказать блюда'),
        BotCommand(command='/cancel', description='Отмена'),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,\
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logger.error('Starting bot')

    # Парсинг файла конфигурации
    config = load_config('config/bot.ini')

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp, config.tg_bot.admin_id)
    register_cb_handlers_edit(dp)
    register_cb_handlers_group_schedule(dp)
    register_handlers_list_class_time(dp)
    register_cb_handlers_teacher_schedule(dp)
    register_handlers_schedule_teachers(dp)
    register_cb_handlers_add_new_group(dp)
    register_cb_handlers_tasks_group(dp)
    register_cb_handlers_tasks_class_time(dp)
    register_cb_handlers_search_group_by_grade(dp)
    register_cb_handlers_add_new_user(dp)
    register_cb_handlers_add_class_time(dp)
    register_cb_handlers_tasks_user(dp)
    register_cb_handlers_tasks_class_room(dp)

    await set_commands(bot)  # Установка команд бота

    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())