from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon import users, tasks
import datetime

router: Router = Router()

@router.message(Command(commands=['start']))
async def command_start(message: Message):
    if message.from_user.id in users and (users[message.from_user.id]['current_task'] == 0 or datetime.datetime.now() >= users[message.from_user.id]['finish_time']):
        if users[message.from_user.id]['current_task'] != 0:
            users[message.from_user.id]['current_task'] = 0
        await message.answer(f'Вы уже проходили испытания. \nВаши баллы: {users[message.from_user.id]["total_score"]}')
    elif message.from_user.id in users and users[message.from_user.id]['current_task'] != 0:
        await message.answer(f'Вы проходите испытания. '
                             f'\nДля получения следующего задания отправьте ответ.')
    else:
        dt1 = datetime.datetime.today()
        dt2 = dt1 + datetime.timedelta(minutes=3)
        print(dt1, dt2)
        users[message.from_user.id] = {'current_task': 0,
                                        'total_score': 0,
                                        'start_time': dt1,
                                        'finish_time': dt2,
                                        1: 0,
                                        2: 0,
                                        3: 0}
        users[message.from_user.id]['current_task'] = 1
        await message.answer(f'Тестирование состоит из 3 задач, \nкоторые надо решить за 3 минуты.'
                             f'\nЗадача №1: {tasks[1][0]}')

@router.message(Command(commands=['help']))
async def command_help(message:Message):
    await message.answer(f'Пройти испытание можно только один раз.'
                         f'\nВремя тестирования - 3 минуты.'
                         f'\nПолучить первое задание можно командой /start.'
                         f'\nОтвет должен быть числом.'
                         f'\nВсе задачи решаются последовательно - '
                         f'\nследующее задание отправится после получения от вас ответа на предыдущее.')