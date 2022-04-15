from aiogram import types, Dispatcher
import create_bot
import init_data
from my_filters import IsNotAdmin
from censure import Censor
from create_bot import dp, bot
import time, string
import inspect
from aiogram.types.message import ContentType


# отправка сообщение и ограничение по времени
async def ban_action_and_msg(tlg_msg, text, ban_msg, ban_time=5):
    try:
        await bot.send_message(init_data.my_god,
                               text=f" @{tlg_msg.from_user.username} написал:{text}\n его забанили")
        await bot.send_message(tlg_msg.chat.id,
                               ban_msg + f"Вы не сможете отправлять собщения в чат {str(ban_time)} минут")
        await bot.restrict_chat_member(tlg_msg.chat.id, tlg_msg.from_user.id, until_date=time.time() + ban_time * 60)
        await tlg_msg.delete()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# обработчик фильтр сылок, матов ,персылок
# @dp.message_handler(IsNotAdmin(), content_types=types.ContentTypes.ANY)
async def moderate_message(msg: types.Message):
    try:
        # check forwarding
        if msg.is_forward():
            await ban_action_and_msg(msg, str(msg), f" @{msg.from_user.username} Пересылка сообщений запрещена.", 5)
            return

        text = ""
        if msg.content_type in {ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT}:
            text += msg.caption
        elif msg.content_type == ContentType.TEXT:
            text += msg.text
        elif msg.content_type == ContentType.NEW_CHAT_MEMBERS:
            await msg.delete()
        else:
            return

        if text == "":
            return

        # check urls
        entities_types = set()
        for entity in msg.entities:
            entities_types.add(entity.type)

        if set(entities_types).intersection(["url", "text_link"]) != set(""):
            await ban_action_and_msg(msg, text, f" @{msg.from_user.username} Отправка ссылок в чат запрещена.", 10)
            # await msg.delete()
            # await bot.send_message(msg.chat.id, f" @{msg.from_user.username} Отправка ссылок в чат запрещена.")
            return

            # check censor
        censor_ru = Censor.get(lang='ru')
        censor_ls = censor_ru.clean_line(text)
        # мат нашелся
        if censor_ls[1] != 0:
            old_ls_text = text.split()
            censor_ls_text = censor_ls[0].split()
            new_msg = list()

            for x in range(len(old_ls_text)):
                if censor_ls_text[x] == "[beep]":
                    new_msg.append("*" * len(old_ls_text[x]))
                else:
                    new_msg.append(old_ls_text[x])
            new_str = " ".join(new_msg)
            # await msg.delete()
            # await bot.send_message(msg.chat.id,
            #                        f" @{msg.from_user.username} написал:\n" + new_str + "\nМат в чате запрещен.")
            await ban_action_and_msg(msg, text,
                                     f" @{msg.from_user.username} написал:\n" + new_str + "\nМат в чате запрещен.",
                                     10)
            return

        if (len({word.lower().translate(str.maketrans('', "", string.punctuation)) for word in
                 text.split(" ")}.intersection(init_data.bad_words)) != 0):
            await ban_action_and_msg(msg, text, f" @{msg.from_user.username} ваше сообщение запрещено.", 10)
            return
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


def register_handlers_censor_handlers(db: Dispatcher):
    pass
    dp.register_message_handler(moderate_message, IsNotAdmin(), content_types=types.ContentTypes.ANY)
