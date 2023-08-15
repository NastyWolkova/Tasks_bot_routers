from aiogram import Router
from aiogram.filters import CommandStart, Text, or_f
from aiogram.types import Message
from lexicon.lexicon import users, tasks, answers
import datetime
from keyboards import keyboard
import surrogates

arrow = surrogates.decode('⬇')

router: Router = Router()


@router.message(or_f(Text(text='Старт'), CommandStart()))
async def command_start(message: Message):
    if message.from_user.id not in users:
        #запуск теста
        dt1 = datetime.datetime.today()
        dt2 = dt1 + datetime.timedelta(minutes=3)
        users[message.from_user.id] = {'current_task': 0,
                                       'total_score': 0,
                                       'start_time': dt1,
                                       'finish_time': dt2,
                                       1: 0,
                                       2: 0,
                                       3: 0}
        users[message.from_user.id]['current_task'] = 1
        print(users)
        await message.answer(f"{answers['start1']} \n{tasks[1][0]}")
    else:
        if users[message.from_user.id]['current_task'] == 0:
            await message.answer(f"{answers['game_over']} {users[message.from_user.id]['total_score']}")
        else:
            if datetime.datetime.now() >= users[message.from_user.id]['finish_time']:
                users[message.from_user.id]['current_task'] = 0
                await message.answer(f"{answers['time_over']} {users[message.from_user.id]['total_score']}")
            else:
                await message.answer(f"{answers['into_game']}")


@router.message(Text(text='Правила'))
async def command_help(message: Message):
    await message.answer(f"{answers['help']}{arrow}", reply_markup=keyboard)