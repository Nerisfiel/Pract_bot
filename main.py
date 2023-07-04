import random
import telebot,sqlite3
from telebot import types
from tasks_checker import TaskChecker

JenPt_bot = telebot.TeleBot('6389247381:AAHYJiB9zYeRLW_3rfauO3btQhetykMqzw0')

@JenPt_bot.message_handler(commands=['start'])
def start(message):
    JenPt_bot.send_message(message.chat.id, "Привет :3")

@JenPt_bot.message_handler(commands=['res'])
def res(message):
    con = sqlite3.connect("JDB.db")
    cursor = con.cursor()
    sqlite_insert_query = """SELECT res FROM test_res WHERE id = """ + str(message.chat.id) + """ and res not in (-1)"""
    txt = cursor.execute(sqlite_insert_query)
    txt = txt.fetchall()
    print(txt)
    ans = 0
    con.close()
    if txt is None:
        ans = 'А вы ничего и не сделали'
    for i in range(0,len(txt)):
        ans = ans + txt[i][0]
    ans = ans /(len(txt))
    JenPt_bot.send_message(message.chat.id, ans)


@JenPt_bot.message_handler(commands=['test'])
def test(message):
    t_id = test_id(message.chat.id)
    if t_id != 0:
        JenPt_bot.send_message(message.chat.id, 'У вас уже есть задание')
    else:
        txt = test_mes(message.chat.id)
        JenPt_bot.send_message(message.chat.id,txt)



@JenPt_bot.message_handler(content_types=['text'])
def check(message):
    t_id = test_id(message.chat.id)
    if t_id == 0:
        JenPt_bot.send_message(message.chat.id, 'Возмите задание с помошью /test')
    else:
        test_cases = test_c(t_id)
        txt = TaskChecker(message.text, test_cases).check()
        if txt == -1:
            JenPt_bot.send_message(message.chat.id, "Ошибка")
        else:
            con = sqlite3.connect("JDB.db")
            cursor = con.cursor()
            sqlite_insert_query = """INSERT INTO test_res VALUES (""" + str(message.chat.id) + """,""" + str(t_id[0]) + """, 01-01-2003, """ + str(txt) + """)"""
            t = cursor.execute(sqlite_insert_query)
            con.commit()
            sqlite_insert_query = """DELETE FROM test_res WHERE id = """ + str(message.chat.id) + """ and res = -1"""
            t = cursor.execute(sqlite_insert_query)
            con.commit()
            con.close()
            JenPt_bot.send_message(message.chat.id,txt)

@JenPt_bot.message_handler(content_types=['sticker'])
def get_id_sticker(message):
    JenPt_bot.send_sticker(message.chat.id, message.sticker.file_id)


def select_rnd(mci):
    i = 0
    rnd = 0
    con = sqlite3.connect("JDB.db")
    cursor = con.cursor()
    sqlite_insert_query = """SELECT test_id FROM test_res WHERE id = """+str(mci)+""";"""
    txt = cursor.execute(sqlite_insert_query)
    abc = txt.fetchall()
    if abc == []:
        return random.randint(1, 2)
    con.close()
    while i < 100:
        r = random.randint(1, 2)
        for j in range(0,len(abc)):
            if r == abc[j][0]:
                r = 0
                break;
        if r != 0:
            rnd = r
            break;
        i = i + 1
    print(rnd)
    return rnd
def test_mes(mci):
    rnd = select_rnd(mci)
    if rnd == 0:
        txt = 'Задания закончились :с'
    else:
        con = sqlite3.connect("JDB.db")
        cursor = con.cursor()
        sqlite_insert_query = """SELECT txt FROM tests WHERE id = """+str(rnd)+""""""
        txt = cursor.execute(sqlite_insert_query)
        txt = txt.fetchone()
        sqlite_insert = """INSERT INTO test_res VALUES (""" + str(mci) + """,""" + str(rnd) + """, 01-01-2003, """ + str(-1) + """)"""
        t = cursor.execute(sqlite_insert)
        con.commit()
        con.close()
    return txt

def test_id(mci):
    con = sqlite3.connect("JDB.db")
    cursor = con.cursor()
    sqlite_insert_query = """SELECT test_id FROM test_res WHERE id = """ + str(mci) + """ and res = -1"""
    txt = cursor.execute(sqlite_insert_query)
    txt = txt.fetchone()
    con.close()
    if txt is None:
        txt = 0
    return txt

def test_c(t_id):
    con = sqlite3.connect("JDB.db")
    cursor = con.cursor()
    sqlite_insert_query = """SELECT res1,res2,res3,res4,res5 FROM tests WHERE id = """ + str(t_id[0]) + """"""
    txt = cursor.execute(sqlite_insert_query)
    txt = txt.fetchone()
    con.close()
    return [(2,3,txt[0]),(6,-2,txt[1]),(889,2345,txt[2]),(73456,23454,txt[3]),(23644,86563,txt[4])]


JenPt_bot.polling()
