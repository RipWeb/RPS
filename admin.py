from aiogram.types import *
from aiogram import Dispatcher
from keyboards import *
from texts import *
from bot import bot
from client import db
from filters import adminFilter
from aiogram.filters.command import Command
from states import Form
from aiogram.fsm.context import FSMContext
import json
import asyncio
import datetime

mail_status = True


async def admin(ctx: Message) -> None:
    await bot.send_message(ctx.chat.id, text="<b>Панель администратора:</b>", reply_markup=admin_kb)
    
async def stat(ctx: CallbackQuery) -> None:
    uc = db.get_all_users_count()[0]
    gc = db.get_all_groups_count()[0]
    uca = db.get_all_users_count_alive()[0]
    gca = db.get_all_groups_count_alive()[0]
    users = db.get_all_users()
    users_day = []
    users_week = []
    users_month = []
    for i in users:
        date = datetime.datetime.strptime(i['join_date'], '%Y, %m, %d, %H, %M')
        td = datetime.datetime.now()-date
        if td.seconds <= 86400:
            users_day.append(i)
        if td.seconds <= 7 * 86400:
            users_week.append(i)
        if td.seconds <= 30 * 86400:
            users_month.append(i)
    count_day = 0
    for i in users_day:
        if db.check_ref(i['user_id'][0]) == None:
            count_day += 1
    count_week = 0
    for i in users_week:
        if db.check_ref(i['user_id'][0]) == None:
            count_week += 1
    count_month = 0
    for i in users_month:
        if db.check_ref(i['user_id'][0]) == None:
            count_month += 1
    
    groups = db.get_all_groups()
    groups_day = []
    groups_week = []
    groups_month = []
    for i in groups:
        date = datetime.datetime.strptime(i['join_date'], '%Y, %m, %d, %H, %M')
        td = datetime.datetime.now()-date
        if td.seconds <= 86400:
            groups_day.append(i)
        if td.seconds <= 7 * 86400:
            groups_week.append(i)
        if td.seconds <= 30 * 86400:
            groups_month.append(i)
    await bot.send_message(ctx.from_user.id, text=stat_text.format(uc,uca, gc, gca, len(users_day), len(users_week), len(users_month),count_day,count_week,count_month,len(groups_day),len(groups_week),len(groups_month)))

async def refs(ctx: CallbackQuery) -> None:
    res = db.get_refs()
    kb = {'inline_keyboard': [[{'text': 'ДОБАВИТЬ РЕФ', 'callback_data': f"add_ref"}]]}
    if res == []:
        await bot.send_message(ctx.message.chat.id, f"<b>Нет рефок =(</b>", reply_markup=kb)
    else:
        text = ''
        count = 0
        for i in res:
            count+=1
            name = i['name'] 
            p = db.get_pass(name)
            text += f"{count}) {i['name']} - {i['count']} 👤 {p[0] / p[1] if p[1] > 0 else 100}% ✅\nhttps://t.me/{URL}?start={i['name']}\n"
        await bot.send_message(ctx.message.chat.id,text=text, reply_markup=kb)

async def add_ref(ctx: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.set_ref)
    await bot.send_message(ctx.message.chat.id, f"<b>Отправьте имя реф ссылки:</b>", reply_markup=cancel_kb)

async def set_ref(ctx: Message, state: FSMContext) -> None:
    await state.clear()
    db.add_ref(ctx.text)
    await bot.send_message(ctx.chat.id, f"<b>Успешно!</b>")

async def mand_sub(ctx: CallbackQuery) -> None:
    res = db.get_channels()
    kb = {'inline_keyboard': [[{'text': 'ДОБАВИТЬ КАНАЛ', 'callback_data': f"add_channel"}]]}
    if res == []:
        await bot.send_message(ctx.message.chat.id, f"<b>Нет каналов =(</b>", reply_markup=kb)
    else:
        count = 0
        text = ''
        for i in res:
            count += 1
            text += f"<b>{count}) {i['title']} - {i['link']} [ID: {i['id']}] {i['count']} 👤</b>\n"
            kb['inline_keyboard'].append([{'text': f'УДАЛИТЬ ID: {i["id"]}', 'callback_data': f"delchan_{i['id']}"}])
        await bot.send_message(ctx.message.chat.id,text=text, reply_markup=kb)

async def add_channel(ctx: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.set_channel)
    await bot.send_message(ctx.message.chat.id, f"<b>Отправьте title - link</b>", reply_markup=cancel_kb)

async def set_channel(ctx: Message, state: FSMContext) -> None:
    try:
        title = ctx.text.split(' - ')[0]
        link = ctx.text.split(' - ')[1]
        db.add_channel(link, title)
        await state.clear()
        await bot.send_message(ctx.chat.id, f"<b>Успешно!</b>")
    except:
        await bot.send_message(ctx.chat.id, f"<b>Неверный формат!\n\nОтправьте в формате Имя - ссылка:</b>")

async def del_chan(ctx: CallbackQuery) -> None:
    db.del_channel(ctx.data[8:])
    await bot.send_message(ctx.from_user.id, f"<b>Успешно!</b>")



async def ads(ctx: CallbackQuery) -> None:
    res = db.check_ads()
    if res == []:
        pass
    else:
        for i in res:
            kb = {'inline_keyboard': [[{'text': 'ИНФО 👁', 'callback_data': f"infoadv_{i['id']}"}, {'text': 'УДАЛИТЬ 🗑', 'callback_data': f"deladv_{i['id']}"}]]}
            await bot.copy_message(ctx.message.chat.id, message_id=i['message_id'], from_chat_id=i['message_chat'], reply_markup=kb)
    await bot.send_message(ctx.message.chat.id, f"<b>Сейчас: {len(res)} показов</b>", reply_markup=add_advert_kb)

async def add_advert(ctx: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.set_advert)
    await bot.send_message(ctx.message.chat.id, f"<b>Отправьте сообщение, которое будет отображться пользователю раз в несколько сообщений:</b>", reply_markup=cancel_kb)

async def set_advert(ctx: Message, state: FSMContext) -> None:
    await state.clear()
    db.add_advert(ctx.message_id, ctx.chat.id, ctx.reply_markup.model_dump_json() if str(ctx.reply_markup) != 'None' else None)
    await bot.send_message(ctx.chat.id, f"<b>Успешно!</b>")

async def del_advert(ctx: CallbackQuery) -> None:
    db.del_adv(ctx.data[7:])
    await ctx.message.delete()

async def info_advert(ctx: CallbackQuery) -> None:
    id = ctx.data[8:]
    info = db.check_advert(id)
    await ctx.answer(f"{info['count']} 👁")

async def greetings(ctx: CallbackQuery) -> None:
    res = db.check_greetings()
    if res == None:
        kb = {'inline_keyboard': [[{'text': 'ДОБАВИТЬ 👋', 'callback_data': f"add_greet"}]]}
        await bot.send_message(ctx.message.chat.id, f"<b>приветки нет =(</b>", reply_markup=kb)
    else:
        kb = {'inline_keyboard': [[{'text': 'ИНФО 👁', 'callback_data': f"infogreet"}, {'text': 'УДАЛИТЬ 🗑', 'callback_data': f"delgreet"}]]}
        rm = json.loads(res['reply_markup']) if res['reply_markup'] != None else None
        await bot.copy_message(ctx.message.chat.id, message_id=res['message_id'], from_chat_id=res['message_chat'], reply_markup=rm)
        await bot.send_message(ctx.message.chat.id, f"<b>🔼 ПРИВЕТСТВИЕ</b>", reply_markup=kb)
    return
    
async def add_greet(ctx: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.set_greetings)
    await bot.send_message(ctx.message.chat.id, f"<b>Отправьте приветствие:</b>", reply_markup=cancel_kb)

async def set_greet(ctx: Message, state: FSMContext) -> None:
    await state.clear()
    db.add_greetings(ctx.message_id, ctx.chat.id, ctx.reply_markup.model_dump_json() if str(ctx.reply_markup) != 'None' else None)
    await bot.send_message(ctx.chat.id, f"<b>Успешно!</b>")

async def del_greet(ctx: CallbackQuery) -> None:
    db.del_greetings()
    await ctx.message.delete()

async def info_greet(ctx: CallbackQuery) -> None:
    info = db.check_greetings()
    await ctx.answer(f"{info['count']} 👁")


async def distribution(ctx: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.set_mail)
    await bot.send_message(ctx.message.chat.id, f"<b>Отправьте пост для рассылки:</b>", reply_markup=cancel_kb)

async def set_mail(ctx: Message, state: FSMContext) -> None:
    await state.clear()
    users = db.get_all_users()
    await bot.send_message(ctx.chat.id, f"✅ Начинаю рассылку. \n\nВсего получателей: {len(users)}")
    count=0
    for user in users:
        if mail_status:
            try:
                await bot.copy_message(chat_id=user[0], from_chat_id=ctx.chat.id, message_id=ctx.message_id, reply_markup=ctx.reply_markup)
                await asyncio.sleep(0.3)
                count+=1
            except: pass
        else: break
    await bot.send_message(ctx.chat.id, f"<b>✅ Рассылка прошла успешно: {count}\nБот заблокирован: {len(users)-count}</b>")

async def cancel(ctx: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await ctx.message.delete()


def reg(dp: Dispatcher):
    dp.message.register(admin, Command('admin'), adminFilter())
    dp.message.register(set_advert, adminFilter(), Form.set_advert)
    dp.message.register(set_greet, adminFilter(), Form.set_greetings)
    dp.message.register(set_channel, adminFilter(), Form.set_channel)
    dp.message.register(set_ref, adminFilter(), Form.set_ref)
    dp.message.register(set_mail, adminFilter(), Form.set_mail)

    dp.callback_query.register(stat, lambda c: c.data == 'statistics')
    dp.callback_query.register(refs, lambda c: c.data == 'referrals')
    dp.callback_query.register(mand_sub, lambda c: c.data == 'mandatory_sub')
    dp.callback_query.register(ads, lambda c: c.data == 'ads')
    dp.callback_query.register(greetings, lambda c: c.data == 'greetings')
    dp.callback_query.register(distribution, lambda c: c.data == 'distribution')

    dp.callback_query.register(add_advert, lambda c: c.data == 'add_advert')
    dp.callback_query.register(del_advert, lambda c: c.data.startswith('deladv_'))
    dp.callback_query.register(info_advert, lambda c: c.data.startswith('infoadv_'))
    dp.callback_query.register(cancel, lambda c: c.data == 'cancel')

    dp.callback_query.register(add_greet, lambda c: c.data == 'add_greet')
    dp.callback_query.register(del_greet, lambda c: c.data == 'delgreet')
    dp.callback_query.register(info_greet, lambda c: c.data == 'infogreet')

    dp.callback_query.register(add_channel, lambda c: c.data == 'add_channel')
    dp.callback_query.register(del_chan, lambda c: c.data.startswith('delchan_'))

    dp.callback_query.register(add_ref, lambda c: c.data == 'add_ref')
