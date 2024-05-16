from typing import Union

from aiogram.filters import Filter
from aiogram.types import *
from bot import ADMINS

class ChatTypeFilter(Filter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, ctx: Message) -> bool:  # [3]
        if isinstance(self.chat_type, str):
            return ctx.chat.type == self.chat_type
        else:
            return ctx.chat.type in self.chat_type

class adminFilter(Filter):  # [1]
    def __init__(self): # [2]
        pass
    async def __call__(self, ctx: Message) -> bool:  # [3]
        return ctx.chat.id in ADMINS