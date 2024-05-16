from aiogram.types import *
URL = 'KamenNozhnitsyBot'

menu_kb = {"keyboard": [
    [{"text": "▶️ ИГРАТЬ СЕЙЧАС"}],
    [{"text": "👤 ПРОФИЛЬ"}, {"text": "🏆 ТОП"}]
    ], 
    "resize_keyboard": True
}

play_kb = {'inline_keyboard': [
    [{'text': '▶️ ИГРАТЬ', 'callback_data': 'play_in_private'}],
    [{'text': '💬 ИГРАТЬ В ЧАТЕ', 'url': f'https://t.me/{URL}?startgroup=AddGroup'}],
    [{'text': '🤠 ИГРАТЬ С ДРУГОМ', 'switch_inline_query_chosen_chat': {'query': 'Отправить вызов:', 'allow_user_chats': True, 'allow_group_chats': True }}]
]}
play_group_kb = {'inline_keyboard': [
    [{'text': '💬 ИГРАТЬ В ЧАТЕ', 'url': f'https://t.me/{URL}?startgroup=AddGroup'}],
    [{'text': '🤠 ИГРАТЬ С ДРУГОМ', 'switch_inline_query_chosen_chat': {'query': 'Отправить вызов:', 'allow_user_chats': True, 'allow_group_chats': True }}]
]}

choise_kb = {'inline_keyboard': [
    [{'text': '1', 'callback_data': 'count_wins_1'}, {'text': '2', 'callback_data': 'count_wins_2'}, {'text': '3', 'callback_data': 'count_wins_3'}],
    [{'text': '4', 'callback_data': 'count_wins_4'}, {'text': '5', 'callback_data': 'count_wins_5'}]
]}

play1_kb = {'inline_keyboard': [
    [{'text': '👉 ИГРАТЬ (0/2)', 'callback_data': 'play_1'}],
]}

def play2_kb(uid):
    return {'inline_keyboard': [
    [{'text': '👉 ИГРАТЬ (1/2)', 'callback_data': f'play_{uid}'}]]}

play3_kb = {'inline_keyboard': [
    [{'text': '👉 ПЕРЕЙТИ К БОТУ ', 'url': f'https://t.me/{URL}'}],
]}


choise_play_kb = {'inline_keyboard': [
    [{'text': '🪨 КАМЕНЬ', 'callback_data': 'chose_rock'}],
    [{'text': '✂️ НОЖНИЦЫ', 'callback_data': 'chose_scissors'}],
    [{'text': '🧻 БУМАГА', 'callback_data': 'chose_paper'}]
]}



#ADMIN 

admin_kb = {'inline_keyboard': [
    [{'text': '📊 СТАТА', 'callback_data': 'statistics'}, {'text': '💎 РЕФЫ', 'callback_data': 'referrals'}],
    [{'text': '🗂 ОП', 'callback_data': 'mandatory_sub'}, {'text': '👁 ПОКАЗЫ', 'callback_data': 'ads'}],
    [{'text': '👋 ПРИВЕТЫ', 'callback_data': 'greetings'}, {'text': '📬 РАССЫЛ', 'callback_data': 'distribution'}]
]}

add_advert_kb = {'inline_keyboard': [
    [{'text': '👁 ДОБАВИТЬ ПОКАЗ', 'callback_data': 'add_advert'}],
]}

cancel_kb = {'inline_keyboard': [
    [{'text': '❌ ОТМЕНА', 'callback_data': 'cancel'}],
]}

