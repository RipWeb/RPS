import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import Database
import datetime
from bot import bot
from texts import *
from keyboards import *


db = Database()

async def remover():
    fights = db.check_time()
    for i in fights:
        date=datetime.datetime.strptime(i['time'], '%Y, %m, %d, %H, %M, %S')
        td = datetime.datetime.now()-date
        if td.seconds > 80:
            db.del_fight(i['id_one'])


async def remover_queue():
        fights = db.check_time_queue()
        for i in fights:
            date=datetime.datetime.strptime(i['time'], '%Y, %m, %d, %H, %M, %S')
            td = datetime.datetime.now()-date
            if td.seconds > 8:
                db.del_queue(i['user_id'])
                await bot.send_message(text=nenaxod_text, chat_id=i['user_id'], reply_markup=play_group_kb)


async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(remover, 'interval', seconds=10)
    scheduler.add_job(remover_queue, 'interval', seconds=8)
    scheduler.start()

    while True:
        await asyncio.sleep(1)