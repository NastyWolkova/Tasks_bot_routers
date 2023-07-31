from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon import users
from config_data.config import load_config

config = load_config('.env')
admin = config.tg_bot.admin_ids[0]

def result_dict(func):
    my_dict: dict = {}
    for key, item in func.items():
        for inkey, initem in item.items():
            if inkey == 'current_task' and initem == 0:
                my_dict[key] = item
    return my_dict

router: Router = Router()
router.message.filter(F.from_user.id == admin)

@router.message(Command(commands=['stat']))
async def command_stat(message:Message):
    await message.answer(f'Data of players: \n{result_dict(users)}')

# @router.message(Command(commands=['cancel']))
# async def command_cancel(message:Message):
#     users: dict = {1111111: {'current_task': 1,
#                              'total_score': 0,
#                              'start_time': 35,
#                              'finish_time': 48,
#                              1: 0,
#                              2: 0,
#                              3: 0}}
#     await message.answer(f'Data of players: \n{result_dict(users)}')

