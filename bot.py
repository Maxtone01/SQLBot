import telebot
import sqlite3
import random as r
import time
from telebot import types

bot = telebot.TeleBot('1096004990:AAFiiaXeTuYYdB7aPJQsNuLSheQBF3OQCzk')
db = sqlite3.connect('Telegram.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               login INTEGER,
               scr INTEGER,
               time TEXT,
               username TEXT
)""")
db.commit()


@bot.message_handler(commands=['reg'])
def start_message(message):
    login = message.from_user.id
    username = message.from_user.username
    scr = 1

    cursor.execute(f"SELECT login FROM users WHERE login = '{login}'")
    if cursor.fetchone() is None:
        a = time.time()
        cursor.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', (login, scr, a, username))
        db.commit()
        bot.send_message(message.chat.id, "Вы зарегистрированы")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы")


@bot.message_handler(commands=['game'])
def start_message(message):
    user_login = message.from_user.id
    user_name = message.from_user.username
    cursor.execute(f'SELECT login FROM users WHERE login = {user_login}')
    for last_update in cursor.execute('SELECT time FROM users'):
        if (time.time() - float(last_update[0])) >= 43200:
            for a in cursor.execute(f"SELECT scr FROM users WHERE login = {user_login}"):
                balance = a[0]
                score = r.randint(-10, 15)
                cursor.execute(f'UPDATE users SET scr = {score + balance} WHERE login = {user_login}')
                db.commit()
                for a in cursor.execute(f'SELECT scr FROM users WHERE login = {user_login}'):
                    pass
                if score > 0:
                    bot.send_message(message.chat.id, "Рексы %s равны %s" % (user_name, a[0]))
                    bot.send_sticker(message.chat.id,
                    "CAACAgIAAxkBAAIOhF9YtnCEc9jKt0d5QYhdW3bQOMA0AAJZAAPNuwMYpOGpdnJ1GQEbBA")
                elif score == 228:
                    bot.send_message(message.chat.id, "Количество рексов игрока %s равно %s, поздравляю, сегодня ты "
                                                      "получишь свой подарок" %(user_name, a[0]))
                    bot.send_sticker(message.chat.id,
                            "CAACAgIAAxkBAAIOkl9YvJ0H3KjKkF5rcM_3BYrrHEmBAAIVAANREZkf7y-q9po-1SkbBA")
                elif score < 0:
                    bot.send_message(message.chat.id, "Количество рексов игрока %s снизилось на %s и стало %s, зачилься"
                                     % (user_name, score, a[0]))
                    bot.send_sticker(message.chat.id,
                                 "CAACAgIAAxkBAAIOhl9YtnaCGBmiM_l8p2zJxEh-ixQ1AAJYAAPNuwMY-uE0fy6-6AcbBA")
        elif (time.time() - float(last_update[0])) <= 43200:
            for a in cursor.execute(f"SELECT scr FROM users WHERE login = {user_login}"):
                for a in cursor.execute(f'SELECT scr FROM users WHERE login = {user_login}'):
                    pass
                bot.send_message(message.chat.id, "Отдохни 12 часов, и возвращайся обратно")
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIOml9Y00X5FHGFtnfWvRwR-jaBCcopAAInAAMwk-4Y9wHdfXkn9tkbBA')


@bot.message_handler(commands=['res'])
def start_message(message):
    sql = "SELECT * FROM users ORDER BY scr DESC LIMIT 15"
    cursor.execute(sql)
    newlist = cursor.fetchall()
    sql_count = "SELECT COUNT(username) FROM users"
    cursor.execute(sql_count)
    count = cursor.fetchone()
    rating = 'Всего: {}\n'.format(count[0])
    i = 1
    for user in newlist:
        rating = rating + str(i) + ": " + str(user[3]) + " - " + str(user[1]) + "\n"
        i += 1
    bot.send_message(message.chat.id, rating)


@bot.message_handler(commands=['dtatadel'])
def start_message(message):
    cursor.execute("DELETE FROM users")
    db.commit()
    bot.send_message(message.chat.id, "Данные удалены")


if __name__ == "__main__":
    bot.polling(none_stop=True)