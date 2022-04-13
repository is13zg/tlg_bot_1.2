from aiogram import types
from aiogram.dispatcher.filters import Filter

import init_data


class IsAdmin(Filter):
    key = "is_admin"

    def ___init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return message.from_user.id in init_data.admins_ids


class IsGod(Filter):
    key = "is_god"

    def ___init__(self, is_god):
        self.is_god = is_god

    async def check(self, message: types.Message):
        return message.from_user.id == init_data.my_god


class IsNotAdmin(Filter):
    key = "is_not_admin"

    def ___init__(self, is_not_admin):
        self.is_not_admin = is_not_admin

    async def check(self, message: types.Message):
        return message.from_user.id not in init_data.admins_ids
