import json
import string, random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import Database

# здесь хранится вся выгрузка книг
data = dict()

# здесь хранится список слов которые забанили админы
bad_words = set()

# здесь хранится список книг для каждого возраста, чтобы не вы бирать каждый раз
book_for_each_ages = dict()
# база данных
db = Database("tlg_bot_database.db")
# shamil_bot_helper
TOKEN = "5102730898:AAHtPPkVYoRnkhgs0kpDB1GL5NhMa64MX4I"
bot_name = "shamil_ahmadullin_helper_bot"
# bot mdrtr
# TOKEN = "5026156622:AAFrtZt7nCRZTtiCYyGJYnCCUWW7Pxvym9E"
# bot_name = "mdrtor123_bot"
# ALLOW_VIDEO=True
# ALLOW_PHOTO=True
# ALLOW_AUDIO=True

# токен чтобы полуить право на админство
my_secret_token = ""
# id создателя
my_god = 97875888

# id админов
admins_ids = {406750498}

question_chat_id = -795883018

UPDATE_FILE_NAME = "books_for_tlg.xlsx"
BOOKS_COUNT_ON_MSG = 6
NONE_SET = {"nan", "None", None, "", " "}
SELECT_AGES = [("0 - 1", "ages_0-1"), ("2 - 3", "ages_2-3"), ("4", "ages_4-4"), ("5", "ages_5-5"),
               ("6 - 7", "ages_6-7"), ("8 - 9", "ages_8-9"), ("10 - 11", "ages_10-11"), ("12 - 14", "ages_12-14"),
               ("14+", "ages_14-18")]
client_ikb2 = InlineKeyboardMarkup()


def update_admins():
    global admins_ids
    admins_ids = set(map(lambda x: x[0], db.get_admins()))


def init_ages_keyboard(client_ikb, SELECT_AGES):
    for x in SELECT_AGES:
        btn = InlineKeyboardButton(text=x[0], callback_data=x[1])
        client_ikb.insert(btn)


def gen_my_secret_token(N=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def gen_books_list(age_text):
    ages = list(map(int, age_text[5:].split("-")))
    result_list = []

    for i, item in enumerate(data["books"]):
        if item["age_min"] <= ages[1] and item["age_max"] >= ages[0]:
            result_list.append(item["books_name"])
    return result_list


def update_dict_with_book_for_each_age():
    global book_for_each_ages
    for x in SELECT_AGES:
        book_for_each_ages[x[1]] = gen_books_list(x[1])


def init_data():
    with open("books.json", "r") as file:
        global data
        data = json.load(file)
        data['books'] = sorted(data["books"], key=lambda tup: tup['order'])

    update_dict_with_book_for_each_age()
    update_admins()

    with open("bad_words.json", "r") as file:
        global bad_words
        bad_words = json.load(file)
        bad_words = set(bad_words["bad_words"])

    init_ages_keyboard(client_ikb2, SELECT_AGES)

    global my_secret_token
    my_secret_token = gen_my_secret_token()
