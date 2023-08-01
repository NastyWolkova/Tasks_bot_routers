from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import users, tasks, answers
import datetime

router: Router = Router()

@router.message(lambda x: x.text and x.text.isdigit())
async def get_answer(message: Message):
    if message.from_user.id not in users:
        await message.answer(f'{answers["not in users"]}')
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
                delta_time = users[message.from_user.id]["finish_time"] - datetime.datetime.today()
                if users[message.from_user.id]['current_task'] == list(tasks.keys())[-1]:
                    users[message.from_user.id]['current_task'] = 0
                    print(users)
                    await message.answer(f'{answers["last_task"]} {users[message.from_user.id]["total_score"]}'
                                         f'\nВремя тестирования: {str(delta_time).split(":")[1].lstrip("0")} мин. {round(float(str(delta_time).split(":")[-1]))} сек.')
                else:
                    #send next task
                    users[message.from_user.id]['current_task'] += 1
                    await message.answer(f'{answers["next_task"]} {users[message.from_user.id]["current_task"]}:\n{tasks[users[message.from_user.id]["current_task"]][0]}'
                                         f'\nУ вас осталось: {str(delta_time).split(":")[1].lstrip("0")} мин. {round(float(str(delta_time).split(":")[-1]))} сек.')

@router.message()
async def send_task(message: Message):
    if message.from_user.id not in users:
        await message.answer(f'{answers["not in users"]}')
    else:
        if users[message.from_user.id]['current_task'] == 0:
            await message.answer(f"{answers['game_over']} {users[message.from_user.id]['total_score']}")
        else:
            if datetime.datetime.now() >= users[message.from_user.id]['finish_time']:
                users[message.from_user.id]['current_task'] = 0
                await message.answer(f"{answers['time_over']} {users[message.from_user.id]['total_score']}")
            else:
                await message.answer(f"{answers['into_game']}")