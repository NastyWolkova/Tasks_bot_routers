from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import users, tasks
import datetime

router: Router = Router()

@router.message(lambda x: x.text and x.text.isdigit())
async def get_answer(message: Message):
    delta_time = users[message.from_user.id]["finish_time"] - datetime.datetime.today()
    # if datetime.datetime.now() < users[message.from_user.id]['finish_time']:
    #     if users[message.from_user.id]['current_task'] != 0 and message.from_user.id in users:
    if datetime.datetime.now() < users[message.from_user.id]['finish_time']:
        if users[message.from_user.id]['current_task'] != 0:
            answer = message.text
            users[message.from_user.id][users[message.from_user.id]['current_task']] = (answer, answer == tasks[users[message.from_user.id]['current_task']][1])
            if answer == tasks[users[message.from_user.id]['current_task']][1]:
                users[message.from_user.id]['total_score'] += tasks[users[message.from_user.id]['current_task']][2]
            if users[message.from_user.id]['current_task'] == list(tasks.keys())[-1]:
                users[message.from_user.id]['current_task'] = 0
                print(users)
                await message.answer(f'Это была последняя задача! \nВаши баллы: {users[message.from_user.id]["total_score"]} '
                                     f'\nВремя тестирования: {str(delta_time).split(":")[1].lstrip("0")} мин. {round(float(str(delta_time).split(":")[-1]))} сек.')
            else:
                users[message.from_user.id]['current_task'] += 1
                await message.answer(f'Ответ принят! '
                                     f'\nCледующая задача №{users[message.from_user.id]["current_task"]}: \n{tasks[users[message.from_user.id]["current_task"]][0]}'
                                     f'\nУ вас осталось: {str(delta_time).split(":")[1].lstrip("0")} мин. {round(float(str(delta_time).split(":")[-1]))} сек.')
        else:
            await message.answer(f'Вы выполнили все задания. '
                                 f'\nВаши баллы: {users[message.from_user.id]["total_score"]}')
    else:
        print(users)
        await message.answer(f'У вас закончилось время тестирования. '
                             f'\nВаши баллы: {users[message.from_user.id]["total_score"]}')

@router.message()
async def send_task(message: Message):
    if message.from_user.id in users:
        if datetime.datetime.now() < users[message.from_user.id]['finish_time']:
            if users[message.from_user.id]['current_task'] != 0:
                await message.answer(f'Вы проходите испытания. \nДля получения следующего задания \nотправьте числовой ответ.')
            else:
                await message.answer(f'Вы выполнили все задания. '
                                     f'\nВаши баллы: {users[message.from_user.id]["total_score"]}')
        else:
            await message.answer(f'У вас закончилось время тестирования. '
                                 f'\nВаши баллы: {users[message.from_user.id]["total_score"]}')
    else:
        await message.answer(f'Для начала испытания используйте команду /start')