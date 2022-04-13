from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import init_data
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# отсылает мне сообщениес
async def send_debug_message(a, b, c):
    await bot.send_message(init_data.my_god, f"module: {a}\nfunc: {b}\nexception: {c}")
    # print(f"module: {a}\nfunc: {b}\nexception: {c}")


storage = MemoryStorage()
bot = Bot(token=init_data.TOKEN, disable_web_page_preview=True)
dp = Dispatcher(bot, storage=storage)
