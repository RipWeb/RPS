import psycopg2
import datetime
import json
from psycopg2.extras import DictCursor
import random
from keyboards import URL

def_dict = {"res1": {"choice1" : '', "choice2": ''}}
def_json = json.dumps(def_dict)



class Database:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host='localhost',
            dbname="rpsdb",
            user="postgres",
            password="1234",
            cursor_factory=DictCursor)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(999), 
                first_name VARCHAR(999), 
                username VARCHAR(999), 
                join_date VARCHAR(999),
                ref_name VARCHAR(999),
                status INTEGER DEFAULT '1',
                invited INTEGER DEFAULT '0',          
                rating INTEGER DEFAULT '0',
                win INTEGER DEFAULT '0', 
                lose INTEGER DEFAULT '0',
                advcount INTEGER DEFAULT '0',
                pass INTEGER DEFAULT '0'
            );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS groups (
                group_id VARCHAR(999),
                status INTEGER DEFAULT '1',
                join_date VARCHAR(999)
            );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS queue (
                user_id VARCHAR(999) UNIQUE,
                time VARCHAR(999)
            );""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS games (
                id_one VARCHAR(999) UNIQUE,
                id_two VARCHAR(999) UNIQUE,
                score1 INTEGER DEFAULT '0',
                score2 INTEGER DEFAULT '0',        
                wins_count INTEGER DEFAULT '1',
                message_id VARCHAR(999),
                turn INTEGER DEFAULT '1',
                round INTEGER DEFAULT '1',
                time VARCHAR(999),
                progress JSONB DEFAULT '{def_json}'
            );""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS rooms (
                chat_id VARCHAR(999),
                id_one VARCHAR(999),
                id_two VARCHAR(999),
                time VARCHAR(999),
                message_id VARCHAR(999)
            );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS channels (
                id SERIAL PRIMARY KEY,
                link VARCHAR(999) NULL,
                title VARCHAR(999) NULL,
                count INTEGER DEFAULT '0'
            );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS referrals (
                id SERIAL PRIMARY KEY, 
                name TEXT, 
                link TEXT, 
                count INTEGER DEFAULT '0'
            );""") 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS advertdata (
                id SERIAL PRIMARY KEY, 
                message_id TEXT,
                message_chat TEXT,
                reply_markup TEXT,
                count INTEGER DEFAULT '0'
            );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS greetingsdata (
                message_id TEXT,
                message_chat TEXT,
                reply_markup TEXT, 
                count INTEGER DEFAULT '0'
            );""")
        

    def get_pass(self, ref_name):
        self.cursor.execute(f"SELECT * FROM users WHERE ref_name = '{ref_name}';")
        res = self.cursor.fetchall()
        count = 0
        for user in res:
            if user['pass'] == 1:
                count+=1
        return(count, len(res))
    
    def check_ref(self, uid):
        self.cursor.execute(f"SELECT ref_name FROM users WHERE user_id = '{uid}';")
        return self.cursor.fetchone()



    #ОП
    def add_channel(self, link, title):
        self.cursor.execute(
            'INSERT INTO channels (link, title) VALUES(%s, %s);', (link, title))

    def get_channels(self):
        self.cursor.execute('SELECT * FROM channels;')
        return self.cursor.fetchall()

    def chan_count(self, link, uid):
        self.cursor.execute(f"UPDATE channels SET count = count + 1 WHERE link = '{link}';")
        self.cursor.execute(f"UPDATE users SET pass = 1 WHERE user_id = '{uid}';")

    def del_channel(self, id):
        self.cursor.execute(f"DELETE FROM channels WHERE id = {id};")
        return 

    #РЕФКИ
    def add_ref(self, name):
        link = f"https://t.me/{URL}?start=ref{name}"
        self.cursor.execute(
            'INSERT INTO referrals (name, link) VALUES(%s, %s);', (name, link))

    def get_refs(self):
        self.cursor.execute('SELECT * FROM referrals;')
        return self.cursor.fetchall()
    
    def ref_count(self, name, uid):
        self.cursor.execute(f"UPDATE referrals SET count = count + 1 WHERE name = '{name}';")
        self.cursor.execute(f"UPDATE users SET ref_name = '{name}' WHERE user_id = '{uid}';")

    #ПОКАЗЫ
    def check_ads(self):
        self.cursor.execute('SELECT * FROM advertdata;')
        return self.cursor.fetchall()
    
    def check_advert(self, id):
        self.cursor.execute(f'SELECT * FROM advertdata WHERE id = {id};')
        return self.cursor.fetchone()
    
    
    def add_advert(self, message_id, message_chat, reply_markup):
        self.cursor.execute(
            'INSERT INTO advertdata (message_id, message_chat, reply_markup) VALUES(%s, %s, %s);', (message_id, message_chat, reply_markup))

    def del_adv(self, id):
        self.cursor.execute(f"DELETE FROM advertdata WHERE id = {id};")
        return 

    
    def advuser(self, uid):
        self.cursor.execute("UPDATE users SET advcount = advcount + 1 WHERE user_id = %s", (str(uid),))

    def check_advcount(self, uid):
        self.cursor.execute(f"SELECT advcount FROM users WHERE user_id = '{uid}';")
        return self.cursor.fetchone()
    
    def randomadv(self):
        self.cursor.execute('SELECT * FROM advertdata')
        result = self.cursor.fetchall()
        res = random.choice(result)
        self.cursor.execute("UPDATE advertdata SET count = count + 1 WHERE id = %s", (res['id'],))
        return res

    #ПРИВЕТЫ
    def check_greetings(self):
        self.cursor.execute('SELECT * FROM greetingsdata;')
        return self.cursor.fetchone()
    
    def add_greetings(self, message_id, message_chat, reply_markup):
        self.cursor.execute(
            'INSERT INTO greetingsdata (message_id, message_chat, reply_markup) VALUES(%s, %s, %s);', (message_id, message_chat, reply_markup))

    def del_greetings(self):
        self.cursor.execute(f"DELETE FROM greetingsdata;")
        return 
    
    def get_greet(self):
        self.cursor.execute("UPDATE greetingsdata SET count = count + 1")
        self.cursor.execute('SELECT * FROM greetingsdata')
        return self.cursor.fetchone()
    

    #ПОЛЬЗОВАТЕЛИ
    def update_data(self, uid, first_name, username):
        self.cursor.execute(f"UPDATE users SET first_name = '{first_name}' WHERE user_id = '{uid}'")
        self.cursor.execute(f"UPDATE users SET username = '{username}' WHERE user_id = '{uid}'")

    def get_all_users_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM users;')
        return self.cursor.fetchone()

    def get_all_groups_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM groups;')
        return self.cursor.fetchone()
    
    def get_all_users_count_alive(self):
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE status = 1;')
        return self.cursor.fetchone()
    
    def get_all_groups_count_alive(self):
        self.cursor.execute('SELECT COUNT(*) FROM groups WHERE status = 1;')
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users;')
        return self.cursor.fetchall()
    
    def get_all_groups(self):
        self.cursor.execute('SELECT * FROM groups;')
        return self.cursor.fetchall()
 

    def add_user(self, user_id, first_name, username):
        date=datetime.datetime.now().strftime('%Y, %m, %d, %H, %M')
        self.cursor.execute(
            'INSERT INTO users (user_id, first_name, username, status, join_date) VALUES(%s,%s,%s,%s,%s);', (user_id, first_name, username, 1, date))
    
    def user_exists(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = %s;', (str(user_id),))
        return bool(len(self.cursor.fetchall()))
 
    def getMe(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = %s;', (str(user_id),))
        res = self.cursor.fetchone()
        return res
    
    def get_top_users(self):
        self.cursor.execute('SELECT * FROM users;')
        res = self.cursor.fetchall()
        res.sort(key=lambda x: x["rating"], reverse=True)
        return res[:10]
    
    def add_group(self, group_id):
        self.cursor.execute(
            'INSERT INTO groups (group_id) VALUES(%s);', (group_id,))
            
    def group_exists(self, group_id):
        self.cursor.execute('SELECT * FROM groups WHERE group_id = %s;', (str(group_id),))
        return bool(len(self.cursor.fetchall()))
    
    def inactive(self, user_id):
        self.cursor.execute(
            'UPDATE users SET status = 0 WHERE user_id = %s', (str(user_id),))

    def active(self, user_id):
        self.cursor.execute(
            'UPDATE users SET status = 1 WHERE user_id = %s', (str(user_id),))   
    
    def inactive_group(self, group_id):
        self.cursor.execute(
            'UPDATE groups SET status = 0 WHERE group_id = %s', (str(group_id),))
    
    def active_group(self, group_id):
        self.cursor.execute(
            'UPDATE groups SET status = 1 WHERE group_id = %s', (str(group_id),))

    # GAME

    def search_enemy(self, user_id):
        self.cursor.execute(f"SELECT * FROM queue WHERE user_id !='{user_id}';")
        return self.cursor.fetchone()

    def del_queue(self, user_id):
        self.cursor.execute(f"DELETE FROM queue WHERE user_id ='{user_id}';")
        return
    
    def add_queue(self, user_id):
        time = datetime.datetime.now().strftime('%Y, %m, %d, %H, %M, %S')
        try:
            self.cursor.execute(
                'INSERT INTO queue (user_id, time) VALUES(%s, %s);', (user_id, time))
            return 1
        except:
            return 0
    
    def add_game(self, id_one, id_two):
        time = datetime.datetime.now().strftime('%Y, %m, %d, %H, %M, %S')
        try:
            self.cursor.execute(
                'INSERT INTO games (id_one, id_two, time) VALUES(%s, %s, %s);', (id_one, id_two, time))
            return
        except Exception as e:
            pass
    
    def add_room(self, chat_id, id_one, id_two, mesid):
        time = datetime.datetime.now().strftime('%Y, %m, %d, %H, %M, %S')
        self.cursor.execute(
            'INSERT INTO rooms (chat_id, id_one, id_two, time, message_id) VALUES(%s, %s, %s, %s, %s);', (chat_id, id_one, id_two, time, mesid))
        return
    
    
    def add_wins_count(self, id_one, wins_count):
        self.cursor.execute(
            f"UPDATE games SET wins_count = '{wins_count}' WHERE id_one = '{id_one}';")
        return

    def update_time(self, id_one, time):
        self.cursor.execute(
            f"UPDATE games SET time = '{time}' WHERE id_one = '{id_one}';")
        return
    
    def info_fight(self, uid):
        self.cursor.execute(f"SELECT * FROM games WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return self.cursor.fetchone()
    
    def check_fight(self, uid):
        self.cursor.execute(f"SELECT * FROM games WHERE id_one ='{uid}' OR id_two ='{uid}';")
        res = self.cursor.fetchone()
        return res
    
    def check_time(self):
        self.cursor.execute(f"SELECT * FROM games;")
        return self.cursor.fetchall()

    def check_time_queue(self):
        self.cursor.execute(f"SELECT * FROM queue;")
        return self.cursor.fetchall()

    def del_fight(self, uid):
        self.cursor.execute(f"DELETE FROM games WHERE id_one ='{uid}' OR id_two ='{uid}';")
        self.cursor.execute(f"SELECT * FROM rooms WHERE id_one ='{uid}' OR id_two ='{uid}';")
        res = self.cursor.fetchone()
        return res
    
    def del_queue(self, uid):
        self.cursor.execute(f"DELETE FROM queue WHERE user_id ='{uid}';")
        return

    def del_room(self, uid):
        self.cursor.execute(f"DELETE FROM rooms WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return 
    
    def update_progress(self, uid, data):
        data = json.dumps(data)
        self.cursor.execute(
            f"UPDATE games SET progress = '{data}' WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return
    
    def update_round(self, uid):
        self.cursor.execute(
            f"UPDATE games SET round = round + 1 WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return
    
    def update_score1(self, uid):
        self.cursor.execute(
            f"UPDATE games SET score1 = score1 + 1 WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return
    
    def update_score2(self, uid):
        self.cursor.execute(
            f"UPDATE games SET score2 = score2 + 1 WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return
    
    def update_mesid(self, uid, message_id):
        self.cursor.execute(
            f"UPDATE games SET message_id = '{message_id}' WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return
    
    def change_turn(self, uid, turn):
        self.cursor.execute(
            f"UPDATE games SET turn = '{turn}' WHERE id_one ='{uid}' OR id_two ='{uid}';")
        return
    
    def get_progress(self, uid):
        self.cursor.execute(
            f"SELECT progress FROM games WHERE id_one = '{uid}' OR id_two ='{uid}';")
        data = json.loads(dict(self.cursor.fetchone()[0]))
        return data
    
    def add_rating(self, user_id, rating):
        self.cursor.execute(f"UPDATE users SET rating = rating + '{rating}' WHERE user_id = '{user_id}' AND rating - '{rating}' > 0;")   