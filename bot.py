import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import others_handlers, commands_handlers, admin_handlers


async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config('.env')
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(admin_handlers.router)
    dp.include_router(commands_handlers.router)
    dp.include_router(others_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())