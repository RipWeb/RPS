from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message
from db import Database

db = Database()

class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        ctx: Message,
        data: Dict[str, Any]
    ) -> Any:
        db.update_data(ctx.from_user.id, ctx.from_user.first_name, ctx.from_user.username)
        await handler(ctx, data)



TOKEN = "6756884476:AAE99S5xxPWnidv86Cu4QeYy06-j5kJHg1M"
ADMINS = [913750670, 767488330]

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))
dp = Dispatcher()
dp.message.outer_middleware(SomeMiddleware())