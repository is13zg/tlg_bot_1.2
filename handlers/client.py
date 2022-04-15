from aiogram import types
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import dp, bot
from my_filters import IsNotAdmin
import math
import init_data
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.message import ContentType
import create_bot
import inspect


class FSMclient(StatesGroup):
    question = State()


async def get_main_id_for_book(book_name):
    try:
        for i, item in enumerate(init_data.data["books"]):
            if item["books_name"] == book_name:
                return i
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


async def get_fast_books_list(age_text):
    try:
        return init_data.book_for_each_ages[age_text]
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


async def send_book(chat_id, book_name="", book_number=-1):
    try:
        if book_number == -1:
            for i, item in enumerate(init_data.data["books"]):
                if book_name == item["books_name"]:
                    book_number = i
                    break;
        msgs_ids = []
        if init_data.data["books"][book_number]["webp_url"] not in {"nan", "None", None}:
            t = await bot.send_message(chat_id=chat_id, text=init_data.data["books"][book_number]["books_name"])
            msgs_ids.append(str(t.message_id))
            t = await bot.send_sticker(chat_id=chat_id, sticker=init_data.data["books"][book_number]["webp_url"])
            msgs_ids.append(str(t.message_id))
        elif init_data.data["books"][book_number]["img_url"] not in {"nan", "None", None}:
            t = await bot.send_photo(chat_id=chat_id, photo=init_data.data["books"][book_number]["img_url"],
                                     caption=init_data.data["books"][book_number]["books_name"])
            msgs_ids.append(str(t.message_id))
        text_with_urls = init_data.data["books"][book_number]["about"]
        temp_inline_markup = InlineKeyboardMarkup(row_width=1)
        if init_data.data["books"][book_number]["wb_url"] not in {"nan", "None", None}:
            text_with_urls += "\n\nКупить на Wb:\n" + init_data.data["books"][book_number]["wb_url"]
            temp_inline_btn1 = InlineKeyboardButton(text="Купить на Wildberies",
                                                    url=init_data.data["books"][book_number]["wb_url"])
            temp_inline_markup.insert(temp_inline_btn1)

        if init_data.data["books"][book_number]["ozon_url"] not in {"nan", "None", None}:
            text_with_urls += "\n\nКупить на Ozon:\n" + init_data.data["books"][book_number]["ozon_url"]
            temp_inline_btn2 = InlineKeyboardButton(text="Купить на Ozon",
                                                    url=init_data.data["books"][book_number]["ozon_url"])
            temp_inline_markup.insert(temp_inline_btn2)

        cancel_btn = InlineKeyboardButton(text="❌", callback_data="delete_msg#" + " ".join(msgs_ids))
        temp_inline_btn3 = InlineKeyboardButton(text="Повторить подбор", callback_data="get_books")
        quest = InlineKeyboardButton(text="Задать вопрос", callback_data="get_question")

        temp_inline_markup.row(temp_inline_btn3, quest)
        temp_inline_markup.row(cancel_btn)
        await bot.send_message(chat_id=chat_id, text=text_with_urls, reply_markup=temp_inline_markup)
        if init_data.db.book_exists(init_data.data["books"][book_number]["books_name"]):
            init_data.db.add_book_view(init_data.data["books"][book_number]["books_name"])
        else:
            init_data.db.add_book(init_data.data["books"][book_number]["books_name"], 1)

    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# удаляет сообщения после нажатия пользователем крестика
# @dp.callback_query_handler(Text(startswith="delete_msg"))
async def process_callback_delete_msg(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.delete()
        ls = callback_query.data.split("#")
        if len(ls) == 2:
            ls = ls[1].split()
            await bot.delete_message(callback_query.message.chat.id, int(ls[0]))
            if len(ls) == 2:
                await bot.delete_message(callback_query.message.chat.id, int(ls[1]))
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# выйдет по нажатию подобрать книги и выдаст список возрастов
# @dp.callback_query_handler(text='get_books')
async def process_callback_choose_ages(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, 'Выберите возраст вашего ребенка',
                               reply_markup=init_data.client_ikb2)
        await callback_query.answer()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# выйдет по нажатию задать вопрос
# @dp.callback_query_handler(text='get_question', state = None)
async def process_callback_get_question_callback(callback_query: types.CallbackQuery):
    try:
        await FSMclient.question.set()
        await bot.send_message(callback_query.from_user.id,
                               'Напишите ваш вопрос и отправьте в чат. Можно отправить текст или изображение.')
        await callback_query.answer()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)

# выйдет по нажатию задать вопрос
async def process_callback_get_question_comand(message: types.Message):
    try:
        await FSMclient.question.set()
        await bot.send_message(message.from_user.id,
                               'Напишите ваш вопрос и отправьте в чат. Можно отправить текст или изображение.')
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# выйдет по нажатию задать вопрос
async def process_choose_books(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Выберите возраст вашего ребенка',
                               reply_markup=init_data.client_ikb2)
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)



# @dp.callback_query_handler(Text(startswith="management#"))
async def process_callback_manage_msg_books(callback_query: types.CallbackQuery):
    try:
        ls = callback_query.data.split("#")
        direction = ls[1]
        pages_count = int(ls[3].split("_")[2])
        page = int(ls[2].split("_")[1])
        if direction == "left":
            if page == 1:
                await callback_query.answer("Ничего не нашлось")
                return
            else:
                page -= 1
        elif direction == "right":
            if page == pages_count:
                await callback_query.answer("Ничего не нашлось")
                return
            else:
                page += 1
        books_ls = await get_fast_books_list(ls[4])
        temp_inline_markup = InlineKeyboardMarkup()
        # вычисляем номера
        last_book_number = 0
        if page == pages_count:
            last_book_number = len(books_ls)
        else:
            last_book_number = init_data.BOOKS_COUNT_ON_MSG * page

        text_books_names_list = f"Результаты {init_data.BOOKS_COUNT_ON_MSG * (page - 1) + 1}-{last_book_number} из {len(books_ls)}\n\n"
        for i, name in enumerate(
                books_ls[init_data.BOOKS_COUNT_ON_MSG * (page - 1):init_data.BOOKS_COUNT_ON_MSG * page]):
            # формируем  список книг для отправки в сообщение
            text_books_names_list += "[" + str(i + 1) + "] " + name + "\n"
            # создаем кнопку для книги с кобэком префиксом buy_book_{номер книги в json}
            temp_inline_btn = InlineKeyboardButton(text=str(i + 1),
                                                   callback_data=f"buy_book_{await get_main_id_for_book(name)}")
            # добавялем кнопку в клавиатуру под сообщение
            temp_inline_markup.insert(temp_inline_btn)

        left_btn = InlineKeyboardButton(text="⬅",
                                        callback_data=f"management#left#page_{page}#" + f"page_count_{pages_count}#" +
                                                      ls[
                                                          4])
        right_btn = InlineKeyboardButton(text="➡",
                                         callback_data=f"management#right#page_{page}#" + f"page_count_{pages_count}#" +
                                                       ls[
                                                           4])
        cancel_btn = InlineKeyboardButton(text="❌", callback_data="delete_msg")
        temp_inline_markup.row(left_btn, cancel_btn, right_btn)

        await callback_query.message.edit_text(
            text='Выберите номер книги которая вас интересует \n\n' + text_books_names_list,
            reply_markup=temp_inline_markup)
        await callback_query.answer("Список книг обновлен")
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# выйдет по нажатию на возраст и выдаст список книг с кнопками(кнопки динамические с префиксом buy_book_{номер книги в json})
# @dp.callback_query_handler(Text(startswith="ages_"))
async def process_callback_get_books(callback_query: types.CallbackQuery):
    try:
        # отберет книги по возрасту
        books_ls = await get_fast_books_list(callback_query.data)
        temp_inline_markup = InlineKeyboardMarkup()
        text_books_names_list = ""
        pages_count = math.ceil(len(books_ls) / init_data.BOOKS_COUNT_ON_MSG)
        if len(books_ls) > (init_data.BOOKS_COUNT_ON_MSG):
            text_books_names_list = f"Результаты 1-{init_data.BOOKS_COUNT_ON_MSG} из {len(books_ls)}\n\n"
            for i, name in enumerate(books_ls[:init_data.BOOKS_COUNT_ON_MSG]):
                # формируем  список книг для отправки в сообщение
                text_books_names_list += "[" + str(i + 1) + "] " + name + "\n"
                # создаем кнопку для книги с кобэком префиксом buy_book_{номер книги в json}
                temp_inline_btn = InlineKeyboardButton(text=str(i + 1),
                                                       callback_data=f"buy_book_{await get_main_id_for_book(name)}")
                # добавялем кнопку в клавиатуру под сообщение
                temp_inline_markup.insert(temp_inline_btn)

            left_btn = InlineKeyboardButton(text="⬅",
                                            callback_data=f"management#left#page_1#" + f"page_count_{pages_count}#" + callback_query.data)
            right_btn = InlineKeyboardButton(text="➡",
                                             callback_data=f"management#right#page_1#" + f"page_count_{pages_count}#" + callback_query.data)
            cancel_btn = InlineKeyboardButton(text="❌", callback_data="delete_msg")
            temp_inline_markup.row(left_btn, cancel_btn, right_btn)

        else:
            for i, name in enumerate(books_ls):
                # формируем  список книг для отправки в сообщение
                text_books_names_list += "[" + str(i + 1) + "] " + name + "\n"
                # создаем кнопку для книги с кобэком префиксом buy_book_{номер книги в json}
                temp_inline_btn = InlineKeyboardButton(text=str(i + 1),
                                                       callback_data=f"buy_book_{await get_main_id_for_book(name)}")
                # добавялем кнопку в клавиатуру под сообщение
                temp_inline_markup.insert(temp_inline_btn)
            cancel_btn = InlineKeyboardButton(text="❌", callback_data="delete_msg")
            temp_inline_btn3 = InlineKeyboardButton(text="Начать подбор снова", callback_data="get_books")
            temp_inline_markup.row(temp_inline_btn3, cancel_btn)

        await bot.send_message(callback_query.from_user.id,
                               'Выберите номер книги которая вас интересует \n\n' + text_books_names_list,
                               reply_markup=temp_inline_markup)
        await callback_query.answer()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# выйдет по нажатию на номер книги в списке и выдаст инфу с книдками
# @dp.callback_query_handler(Text(startswith="buy_book_"))
async def process_callback_show_book(callback_query: types.CallbackQuery):
    try:
        book_id = int(callback_query.data[9:])
        await send_book(chat_id=callback_query.from_user.id, book_number=book_id)
        await callback_query.answer()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# @dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), IsNotAdmin(), content_types=types.ContentTypes.ANY)
async def question_handler(message: types.Message, state: FSMContext):
    try:
        # сделать обработку фото
        text = f"user_id={message.from_user.id}\nmsg_id={message.message_id}\nПользователь {message.from_user.first_name} {message.from_user.last_name} задает вопрос:\n"

        if message.content_type == ContentType.PHOTO:
            await bot.send_photo(chat_id=init_data.question_chat_id, caption=text, photo=message.photo[0].file_id)
        elif message.content_type == ContentType.TEXT:
            await bot.send_message(chat_id=init_data.question_chat_id, text=text + message.text)
        else:
            await message.reply("Вы отправили данные друго типа. Повторите попытку.")
            return

        client_ikb1 = InlineKeyboardMarkup()
        ib1 = InlineKeyboardButton(text="Подобрать пособие", callback_data="get_books")
        client_ikb1.add(ib1)
        ib2 = InlineKeyboardButton(text="Задать вопрос Ш.Ахмадуллину.", callback_data="get_question")
        client_ikb1.add(ib2)
        await message.reply("Ваш вопрос получен. Ответ будет отправлен сюда в чат. Что бы вы хотели?",
                            reply_markup=client_ikb1)
        await state.finish()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# @dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    try:
        if not init_data.db.user_exists(message.from_user.id):
            init_data.db.add_user(message.from_user.id)
        client_ikb1 = InlineKeyboardMarkup()
        ib1 = InlineKeyboardButton(text="Подобрать пособие", callback_data="get_books")
        client_ikb1.add(ib1)
        ib2 = InlineKeyboardButton(text="Задать вопрос Ш.Ахмадуллину.", callback_data="get_question")
        client_ikb1.add(ib2)
        try:
            await bot.send_message(message.from_user.id, "Добрый день. Что бы вы хотели? ", reply_markup=client_ikb1)
        except:
            await message.reply(f"Используйте функции бота через ЛС, напишите сюда\n https://t.me/{init_data.bot_name}")
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)

# @dp.message_handler(commands=['help'])
async def process_help(message: types.Message):
    try:
        text = "Данный телеграм бот может помочь вам подобрать книги или задать вопрос Ш.Ахмадуллину."
        try:
            await bot.send_message(message.from_user.id, text)
        except:
            await message.reply(f"Используйте функции бота через ЛС, напишите сюда\n https://t.me/{init_data.bot_name}")
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# # обработчик запрет видео
# @dp.message_handler(IsNotAdmin(), content_types=["video"])
# async def moderate_video(msg: types.Message):
#     await bot.send_message(msg.chat.id, f" @{msg.from_user.username} Отправка видео запрещена.")
#     await msg.delete()
#
#
# # обработчик запрет фото
# @dp.message_handler(IsNotAdmin(), content_types=["photo"])
# async def moderate_photo(msg: types.Message):
#     await bot.send_message(msg.chat.id, f" @{msg.from_user.username} Отправка изображений запрещена.")
#     await msg.delete()
#
# # обработчик запрет аудио
# @dp.message_handler(IsNotAdmin(), content_types=["audio"])
# async def moderate_photo(msg: types.Message):
#     await bot.send_message(msg.chat.id, f" @{msg.from_user.username} Отправка изображений запрещена.")
#     await msg.delete()

def register_handlers_client(db: Dispatcher):
    dp.register_message_handler(process_start, commands=['start'])
    dp.register_message_handler(process_help, chat_type=types.ChatType.PRIVATE, commands=['help'])
    dp.register_message_handler(process_choose_books, chat_type=types.ChatType.PRIVATE, commands=['choose_books'])
    dp.register_message_handler(process_callback_get_question_comand, chat_type=types.ChatType.PRIVATE, commands=['ask_question'])

    dp.register_callback_query_handler(process_callback_show_book, Text(startswith="buy_book_"))
    dp.register_callback_query_handler(process_callback_get_books, Text(startswith="ages_"))
    dp.register_callback_query_handler(process_callback_manage_msg_books, Text(startswith="management#"))
    dp.register_callback_query_handler(process_callback_choose_ages, text='get_books')
    dp.register_callback_query_handler(process_callback_get_question_callback, text='get_question', state=None)
    dp.register_callback_query_handler(process_callback_delete_msg, Text(startswith="delete_msg"))
    dp.register_message_handler(question_handler, chat_type=types.ChatType.PRIVATE,
                                content_types=types.ContentTypes.ANY, state=FSMclient.question)
