from aiogram.utils import executor

from userBot import config, handler


async def on_startup(dp):
    await config.storage.init(config.DB_URL)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def launch_user_bot():
    executor.start_polling(handler.dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    launch_user_bot()