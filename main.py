import asyncio
import client, admin
from bot import *
from scheduler import start_scheduler
from aiogram.methods import DeleteWebhook

async def main() -> None:
    asyncio.create_task(start_scheduler())
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    client.reg(dp)
    admin.reg(dp)
    asyncio.run(main())