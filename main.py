import requests

from aiogram.utils.executor import start_webhook

from bot.userBot import config, handler


async def on_startup(dp):
    await config.storage.init(config.DB_URL)
    await config.bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    await config.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


def launch_user_bot():
    start_webhook(
        dispatcher=handler.dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )


if __name__ == '__main__':
    isSet = requests.post(
        f"https://api.telegram.org/{config.API_TOKEN_USER_BOT}/setwebhook?url={config.WEBHOOK_URL}"
    )
    launch_user_bot()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
