telegram bot for Language Studio 'Alias'

[![python](https://img.shields.io/badge/python-3.11-green)](https://img.shields.io/badge/python-3.11-green) [![aiogram](https://img.shields.io/badge/aiogram-2.25.1-green)](https://img.shields.io/badge/aiogram-2.25.1-green) [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.7-green)](https://img.shields.io/badge/SQLAlchemy-2.0.7-green)

[![codewars](https://www.codewars.com/users/Kazykan/badges/small)](https://www.codewars.com/users/Kazykan/)

bot написан на aiogram & sqlalchemy

bot commands:

- `/start` — welcome message
- `Подобрать расписание` — выводится опросник какой класс и список подходящих групп с расписание и заполненностью группы
- `Ученику - расписание` — ученик так же выбирает группу и ему приходит уведомление о расписании и времени занятий
- `Учителю` — тут имеем возможность доб. удалять: группы, время занятий, учеников и заполненностью групп

## Задачи

- отправка сообщений в канал файл cb_search_group_by_grade (bot.send_message(CHANNEL_ID, text))