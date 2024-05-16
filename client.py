from aiogram.types import *
from aiogram import Dispatcher, BaseMiddleware
from keyboards import *
from texts import *
from bot import bot
from aiogram.filters.command import Command
from db import Database
from aiogram.fsm.context import FSMContext
from states import Form
import datetime
from filters import *
import json
import asyncio

db = Database()
MAIN_IMG = 'https://telegra.ph/file/383e064f6f7d58c384f06.jpg'

def calc_winner(choice1, choice2):
    if (choice1 == 'rock' and choice2 == 'scissors'):
        return 1
    elif choice1 == 'scissors' and choice2 == 'paper':
        return 1
    elif choice1 == 'paper' and choice2 == 'rock':
        return 1
    elif choice1 == 'rock' and choice2 == 'rock':
        return 0
    elif choice1 == 'scissors' and choice2 == 'scissors':
        return 0
    elif choice1 == 'paper' and choice2 == 'paper':
        return 0
    return 2

#ПОКАЗЫ
async def adgive(chat_id):
    if len(db.check_ads()) < 1:
        return
    db.advuser(chat_id)
    if int(db.check_advcount(chat_id)[0]) % 5 == 0:
        advmessage=db.randomadv()
        kb = json.loads(advmessage['reply_markup']) if advmessage['reply_markup'] != None else None
        await bot.copy_message(from_chat_id=advmessage['message_chat'], message_id=advmessage['message_id'], chat_id=chat_id, reply_markup=kb)

#ПРИВЕТЫ
async def greetgive(chat_id):
    if db.check_greetings() == None:
        return
    else:
        greetings=db.get_greet()
        kb = json.loads(greetings['reply_markup']) if greetings['reply_markup'] != None else None
        await bot.copy_message(from_chat_id=greetings['message_chat'], message_id=greetings['message_id'], chat_id=chat_id, reply_markup=kb)
        await asyncio.sleep(1)

#ОП
def sub_keyboard():
    res = db.get_channels()
    kb = {'inline_keyboard': []}
    for i in res:
        kb['inline_keyboard'].append([{'text': f"{i['title']}", 'url': f"{i['link']}"}])
    kb['inline_keyboard'].append([{'text': 'Проверить ✅', 'callback_data': 'check_subs'}])
    return kb

async def sub_query(ctx: CallbackQuery, state: FSMContext):
        notsubscribe = False
        for channel in db.get_channels():
            try: 
                username = '@' + channel['link'].split('https://t.me/')[1]
                user_channel_status = await bot.get_chat_member(chat_id=username, user_id=ctx.message.chat.id)
                if user_channel_status.status == 'left':
                    notsubscribe = True
                else:
                    db.chan_count(channel['link'], ctx.from_user.id)
            except:
                pass
        if notsubscribe == False:
            await state.clear()
            await ctx.message.answer('Вы подписались 👍')
            try: await ctx.message.delete()
            except: pass
        else:
            await ctx.answer("Вы не подписались на один из каналов!", True)

async def sub_msg(ctx: CallbackQuery):
    await bot.send_message(ctx.from_user.id, '<b>Чтобы играть нужно быть подписаным на эти каналы:</b>', reply_markup=sub_keyboard())

async def subcheck(user_id):
    notsubscribe = False
    for channel in db.get_channels():
        try:
            username = '@' + channel['link'].split('https://t.me/')[1]
            user_channel_status = await bot.get_chat_member(chat_id=username, user_id=user_id)
            if user_channel_status.status == 'left':
                notsubscribe = True
        except:
            pass
    return notsubscribe

async def start(ctx: Message) -> None:
    if ctx.chat.type == 'private':
        if not db.user_exists(ctx.chat.id):
            db.add_user(ctx.chat.id, ctx.from_user.first_name, ctx.from_user.username)
            try:
                db.ref_count(ctx.text.split(" ")[1], ctx.from_user.id)
            except:
                pass
        await greetgive(ctx.chat.id)
        await bot.send_sticker(ctx.chat.id, 'CAACAgIAAxkBAAEMCoFmM645apfOpj-1951eFSIkZi_tIwACBgEAAladvQpU6_CTffOW6zQE', reply_markup=menu_kb)
        await bot.send_photo(ctx.chat.id, photo=MAIN_IMG,caption=play_text, reply_markup=play_kb)
    else:
        await bot.send_message(ctx.chat.id, text=greet_text, reply_markup=play_group_kb)
    

async def play_in_private(ctx: CallbackQuery) -> None:
    if not await subcheck(ctx.from_user.id):
        enemy = db.search_enemy(ctx.message.chat.id)
        if db.check_fight(ctx.message.chat.id) == None:
            if enemy == None:
                if db.add_queue(ctx.message.chat.id):
                    await bot.send_message(ctx.message.chat.id, text="<b>Ищем соперника...</b>")
                else:
                    await bot.send_message(ctx.message.chat.id, text="<b>Вы уже ищете соперника!</b>")
            else:
                db.del_queue(enemy["user_id"]) 
                db.add_game(ctx.message.chat.id, enemy["user_id"])
                await bot.send_message(ctx.message.chat.id, text="<b>До скольки побед играем? 👇</b>", reply_markup=choise_kb)
                await bot.send_message(enemy["user_id"], text="<b>Соперник выбирает кол-во игр...</b>")
        else:
            await bot.send_message(ctx.message.chat.id, text="<b>Вы уже в игре!</b>")
    else:
        await sub_msg(ctx)    


async def create_fight(ctx: CallbackQuery) -> None:
    wins_count = int(ctx.data[11:])
    db.add_wins_count(ctx.from_user.id, wins_count)
    db.update_time(ctx.from_user.id, time=datetime.datetime.now().strftime('%Y, %m, %d, %H, %M, %S'))
    info = db.info_fight(ctx.from_user.id)
    me = db.getMe(info["id_one"])
    enemy = db.getMe(info["id_two"])
    await ctx.message.edit_text(text=duel_text(me["first_name"], enemy["first_name"], me["username"], enemy["username"],
                                               wins_count, 0, 0, 1, info["progress"], info["round"], 1), reply_markup=choise_play_kb)
    msg = await bot.send_message(enemy["user_id"], text=duel_text(me["first_name"], enemy["first_name"], me["username"], enemy["username"],
                                               wins_count, 0, 0, 1, info["progress"], info["round"], 2))
    db.update_mesid(ctx.from_user.id, msg.message_id)
    
    
async def attack(ctx: CallbackQuery) -> None:
    choice = ctx.data[6:]
    info = db.info_fight(ctx.from_user.id)
    score1 = info["score1"]
    score2 = info["score2"]
    turn_cur = info["turn"]
    turn_new = 2 if turn_cur == 1 else 1
    progress = info["progress"]
    progress[f"res{info['round']}"][f"choice{turn_cur}"] = choice
    me = db.getMe(info["id_one"])
    enemy = db.getMe(info["id_two"])
    if str(ctx.from_user.id) == info["id_one"]:
        enemy_id = db.getMe(info["id_two"])
        player1 = 1
        player2 = 2
    else:
        enemy_id = db.getMe(info["id_one"])
        player1 = 2
        player2 = 1
    if progress[f"res{info['round']}"][f"choice{turn_cur}"] != '' and progress[f"res{info['round']}"][f"choice{turn_new}"] != '':
        progress[f"res{info['round'] + 1}"] = {"choice1": '', "choice2": ''}
        db.update_round(ctx.from_user.id)
        winner = calc_winner(progress[f"res{info['round']}"]["choice1"], progress[f"res{info['round']}"]["choice2"])
        if winner == 1:
            score1 += 1 
            db.update_score1(ctx.from_user.id)
        elif winner == 2:
            score2 += 1
            db.update_score2(ctx.from_user.id)
        else:
            pass
        info_text1 = duel_text(me["first_name"], enemy["first_name"], me["username"], enemy["username"], info["wins_count"], score1, score2, turn_new, progress, info["round"], 1)
        info_text2 = duel_text(me["first_name"], enemy["first_name"], me["username"], enemy["username"], info["wins_count"], score1, score2, turn_new, progress, info["round"], 2)
        if score1 >= info["wins_count"]:
            res = db.del_fight(enemy_id['user_id'])
            db.del_room(ctx.from_user.id)
            await ctx.message.edit_text(text=info_text2)
            await bot.edit_message_text(chat_id=enemy_id['user_id'], message_id=info["message_id"], text=info_text1)
            if res != None:
                try:
                    await bot.edit_message_text(chat_id=res['chat_id'], message_id=res["message_id"], text=info_text1)
                except:
                    await bot.edit_message_text(inline_message_id=res["message_id"], text=info_text1)
            return
        elif score2 >= info["wins_count"]:
            res = db.del_fight(ctx.from_user.id)
            db.del_room(ctx.from_user.id)
            await ctx.message.edit_text(text=info_text2)
            await bot.edit_message_text(chat_id=enemy_id['user_id'], message_id=info["message_id"], text=info_text1)
            if res != None:
                try:
                    await bot.edit_message_text(chat_id=res['chat_id'], message_id=res["message_id"], text=info_text1)
                except:
                    await bot.edit_message_text(inline_message_id=res["message_id"], text=info_text1)
            return
        else:
            pass
    info_text1 = duel_text(me["first_name"], enemy["first_name"], me["username"], enemy["username"], info["wins_count"], score1, score2, turn_new, progress, info["round"], player1)
    info_text2 = duel_text(me["first_name"], enemy["first_name"], me["username"], enemy["username"], info["wins_count"], score1, score2, turn_new, progress, info["round"], player2)
    db.change_turn(ctx.from_user.id, turn_new)
    db.update_progress(ctx.from_user.id, progress)
    msg = await ctx.message.edit_text(text=info_text1)
    db.update_mesid(ctx.from_user.id, msg.message_id)
    await bot.edit_message_text(chat_id=enemy_id['user_id'], message_id=info["message_id"],text=info_text2, reply_markup=choise_play_kb)

async def play(ctx: Message) -> None:
    if ctx.chat.type != 'private':
        await bot.send_message(ctx.chat.id, text="<b>⁠⁠ВЫЗОВ ✊ ✌️ ✋</b>\n\n<code>Жми кнопку ниже:</code>", link_preview_options={ "is_disabled": False, 'url': MAIN_IMG}, reply_markup=play1_kb)
    else:
        await adgive(ctx.chat.id)
        await bot.send_photo(ctx.chat.id, photo=MAIN_IMG,caption=play_text, reply_markup=play_kb)

async def add1_player(ctx: CallbackQuery) -> None:
    if ctx.message == None:
        await bot.edit_message_text(inline_message_id=ctx.inline_message_id,text=f"<b>⁠⁠ВЫЗОВ ✊ ✌️ ✋\n\nИГРОК 1: {ctx.from_user.first_name}</b>\n\n<code>Жми кнопку ниже:</code>", link_preview_options={ "is_disabled": False, 'url': MAIN_IMG}, reply_markup=play2_kb(ctx.from_user.id))
    else:
        await ctx.message.edit_text(text=f"<b>⁠⁠ВЫЗОВ ✊ ✌️ ✋\n\nИГРОК 1: {ctx.from_user.first_name}</b>\n\n<code>Жми кнопку ниже:</code>", link_preview_options={ "is_disabled": False, 'url': MAIN_IMG}, reply_markup=play2_kb(ctx.from_user.id))

async def add2_player(ctx: CallbackQuery) -> None:
    if ctx.data[5:] != str(ctx.from_user.id):
        info = db.getMe(ctx.data[5:])
        try:
            db.add_game(ctx.data[5:], ctx.from_user.id)
        except:
            await ctx.answer("Вы уже в бою!")
        await bot.send_message(ctx.data[5:], text="<b>До скольки побед играем? 👇</b>", reply_markup=choise_kb)
        await bot.send_message(ctx.from_user.id, text="<b>Соперник выбирает кол-во игр...</b>")
        if ctx.message != None:
            msg = await ctx.message.edit_text(text=f"<b>⁠⁠ВЫЗОВ ✊ ✌️ ✋\n\nИГРОК 1: {info['first_name']}\nИГРОК 2: {ctx.from_user.first_name}</b>\n\n<code>Жми кнопку ниже:</code>", link_preview_options={ "is_disabled": False, 'url': MAIN_IMG}, reply_markup=play3_kb)
            msg_id = msg.message_id
        else:
            await bot.edit_message_text(inline_message_id=ctx.inline_message_id, text=f"<b>⁠⁠ВЫЗОВ ✊ ✌️ ✋\n\nИГРОК 1: {info['first_name']}\nИГРОК 2: {ctx.from_user.first_name}</b>\n\n<code>Жми кнопку ниже:</code>", link_preview_options={ "is_disabled": False, 'url': MAIN_IMG}, reply_markup=play3_kb)
            msg_id = ctx.inline_message_id
        db.add_room(ctx.from_user.id ,ctx.data[5:], ctx.from_user.id, msg_id)
    else:
        await ctx.answer('Вы уже присоеденились!')


async def profile(ctx: Message) -> None:
    await adgive(ctx.from_user.id)
    info = db.getMe(ctx.from_user.id)
    await bot.send_message(ctx.chat.id, text=profile_text(info['first_name'], info['username'], info['win'], info['lose'], info['rating']))


async def top(ctx: Message) -> None:
    await adgive(ctx.from_user.id)
    users = db.get_all_users()[:10]
    users = sorted(users, key=lambda c: c[0][7], reverse=True)
    count = 0
    text = ''
    while count < len(users):
        text += f'<b>{count + 1}. <a href="https://t.me/{users[count][2]}">{users[count][1]}</a> - {users[count][7]} 🎖️</b>\n'
        count += 1
    await bot.send_message(ctx.chat.id, text=text)

async def sendDuel(ctx: InlineQuery):
    result = []
    result.append({ 
        "type" : "photo", 
        "id" : f"10000", 
        'photo_url' : MAIN_IMG,
        'thumbnail_url' : MAIN_IMG,
        "reply_markup": play1_kb,
        "input_message_content" : { "message_text": "<b>⁠⁠ВЫЗОВ ✊ ✌️ ✋</b>\n\n<code>Жми кнопку ниже:</code>",
                                   "link_preview_options":  { "is_disabled": False, 'url': MAIN_IMG} }})
    await ctx.answer(results=result, cache_time=0)


async def handler(ctx: ChatMemberUpdated) -> None:
    status = ctx.new_chat_member.status.value
    if ctx.chat.type == 'private':
        if status == "kicked":
            db.inactive(ctx.chat.id)
        else:
            db.active(ctx.chat.id)
    else:
        if status == 'member':
            if not db.group_exists(ctx.chat.id):
                db.add_group(ctx.chat.id)
            db.active_group(ctx.chat.id)
        else:
            db.inactive_group(ctx.chat.id)
        

def reg(dp: Dispatcher):
    dp.message.register(start,Command("start"))
    dp.message.register(play, Command("play"))
    dp.message.register(profile, Command("profile"))
    dp.message.register(top, Command("top"))

    dp.message.register(play, lambda c: c.text == '▶️ ИГРАТЬ СЕЙЧАС')
    dp.message.register(profile, lambda c: c.text == '👤 ПРОФИЛЬ')
    dp.message.register(top, lambda c: c.text == '🏆 ТОП')
    
    dp.callback_query.register(play_in_private, lambda c: c.data == 'play_in_private')
    dp.callback_query.register(create_fight, lambda c: c.data.startswith('count_wins_'))
    dp.callback_query.register(attack, lambda c: c.data.startswith('chose_'))
    dp.callback_query.register(add1_player, lambda c: c.data.startswith('play_1'))
    dp.callback_query.register(add2_player, lambda c: c.data.startswith('play_'))

    dp.callback_query.register(sub_query, lambda c: c.data == 'check_subs')
    dp.my_chat_member.register(handler)

    dp.inline_query.register(sendDuel, lambda c: c.query == "Отправить вызов:")
