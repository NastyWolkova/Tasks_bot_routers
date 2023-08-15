from aiogram import Router
from aiogram.types import Message
from keyboards import keyboard
from lexicon.lexicon import users, tasks, answers
import datetime
import surrogates

arrow = surrogates.decode('⬇')

router: Router = Router()

def conv_time(my_time: datetime.timedelta) -> str:
    minute = str(my_time).split(":")[1].lstrip("0")
    sec = round(float(str(my_time).split(":")[-1]))
    if minute:
        out_time: str = f'{minute} мин. {sec} сек.'
    else:
        out_time: str = f'{sec} сек.'
    return out_time


@router.message(lambda x: x.text and x.text.isdigit())
async def get_answer(message: Message):
    if message.from_user.id not in users:
        await message.answer(f'{answers["not in users"]} {arrow}', reply_markup=keyboard)
    else:
        if users[message.from_user.id]['current_task'] == 0:
            await message.answer(f"{answers['game_over']} {users[message.from_user.id]['total_score']}")
        else:
            if datetime.datetime.now() >= users[message.from_user.id]['finish_time']:
                users[message.from_user.id]['current_task'] = 0
                await message.answer(f"{answers['time_over']} {users[message.from_user.id]['total_score']}")
            else:
                answer = message.text
                #add in dict users answers of user and true/false
                users[message.from_user.id][users[message.from_user.id]['current_task']] = (answer, answer == tasks[users[message.from_user.id]['current_task']][1])
                if answer == tasks[users[message.from_user.id]['current_task']][1]:
                    #начисление баллов
                    users[message.from_user.id]['total_score'] += tasks[users[message.from_user.id]['current_task']][2]
                #check on last task
                spare_time = users[message.from_user.id]["finish_time"] - datetime.datetime.today()
                elapsed_time = datetime.datetime.today() - users[message.from_user.id]['start_time']
                if users[message.from_user.id]['current_task'] == list(tasks.keys())[-1]:
                    users[message.from_user.id]['current_task'] = 0
                    await message.answer(f'{answers["last_task"]} {users[message.from_user.id]["total_score"]}'
                                         f'\nВремя тестирования: {conv_time(elapsed_time)}')
                else:
                    #send next task
                    users[message.from_user.id]['current_task'] += 1
                    await message.answer(f'{answers["next_task"]} {users[message.from_user.id]["current_task"]}:\n{tasks[users[message.from_user.id]["current_task"]][0]}'
                                         f'\nУ вас осталось: {conv_time(spare_time)}')


@router.message()
async def send_task(message: Message):
    if message.from_user.id not in users:
        await message.answer(f'{answers["not in users"]} {arrow}', reply_markup=keyboard)
    else:
        if users[message.from_user.id]['current_task'] == 0:
            await message.answer(f"{answers['game_over']} {users[message.from_user.id]['total_score']}")
        else:
            if datetime.datetime.now() >= users[message.from_user.id]['finish_time']:
                users[message.from_user.id]['current_task'] = 0
                await message.answer(f"{answers['time_over']} {users[message.from_user.id]['total_score']}")
            else:
                await message.answer(f"{answers['into_game']}")
