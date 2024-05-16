play_text = f'''<b>Привет! Я бот для игры в 🪨 ✂️ 🧻
Сыграем? Жми👇</b>'''

score_sign = {
    0: '0️⃣',
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
}

sign = {
    'rock': "🪨",
    'scissors': "✂️",
    'paper': "🧻"
}

def duel_text(name1, name2, username1, username2, wins_count, score1, score2, turn, progress, round, a):
    text = f'''<b>ДУЭЛЬ ⚔️\n\n<a href="https://t.me/{username1}">{name1}</a> vs <a href="https://t.me/{username2}">{name2}</a>\n\n{score_sign[score1]} : {score_sign[score2]}  <i>до {wins_count} побед</i></b>'''
    bar_text = ''
    try:
        for i in range(1, round + 1):
            bar_text += f"\n{i}) {sign[progress[f'res{i}']['choice1']]} vs {sign[progress[f'res{i}']['choice2']]}"
    except:
        pass
    if score1 == wins_count:
        chose_pan_text = f'\n\n<b><a href="https://t.me/{username1}">{name1}</a> победил!</b>'
    elif score2 == wins_count:
        chose_pan_text = f'\n\n<b><a href="https://t.me/{username2}">{name2}</a> победил!</b>'
    else:
        if turn == 1 and a == 1 or turn == 2 and a == 2:
            chose_pan_text = '\n\n<b>Вы выбираете 👇</b>'
        else:
            chose_pan_text = '\n\n<b>Соперник выбирает..</b>'
    text = text + bar_text + chose_pan_text
    return text

def profile_text(name, username, win, lose, rating):
    return f'''<b><a href="https://t.me/{username}">{name}</a>

▶️ ИГР СЫГРАНО: {win + lose}
💯 ДОЛЯ ПОБЕД: {win / (win + lose) if (win + lose) > 0 else 0}
🎖️ РЕЙТИНГ: {rating}

⭐️ ПОБЕД: {win}
🤕 ПОРАЖЕНИЙ: {lose}
</b>'''

greet_text = '''<b>Привет 👋
Я - бот для игры в Камень Ножницы Бумага

/play - играть сейчас ▶️
/profile - мой профиль 👤
/top - топ лучших 🏆
</b>'''

nenaxod_text = '''<b>😕 УПС, ИГРА НЕ НАЙДЕНА</b>

Попробуй снова чуть позже'''

stat_text = '''<b>👤 Всего пользователей: {}
🙎‍♂️ Живых пользователей: {}
☁️ Всего групп: {}
💬 Живых групп: {}

Cегодня / неделя / месяц:
• Прирост: {} / {} / {}
• Саморост: {} / {} / {}
• Групп: {} / {} / {}</b>'''