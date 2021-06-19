import requests
from bs4 import BeautifulSoup
from aiogram import Dispatcher, Bot, executor, types
from config import BOT_TOKEN, ADMIN_ID, SITE_LINK, ADMIN_NAME
import sqlite3
import lxml
import logging
import asyncio
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from pprint import pprint

logging.basicConfig(level=logging.INFO)

# create db
db = sqlite3.connect("db.db")
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id TEXT,
    name TEXT
)""")
db.commit()

# bot
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def get_start(msg: types.Message):
    user_id = str(msg.from_user.id)
    name = msg.from_user.first_name
    sub_buttons = ["on", "off"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*sub_buttons)
    await bot.send_photo(msg.from_user.id,
                         photo="https://fiverr-res.cloudinary.com/t_main1,q_auto,f_auto,q_auto,"
                               "f_auto/gigs/129258377/original/678eaed5d12dfcab0f20d0a3d3bcdc4785afb4d5.png")
    await msg.answer(f"Привет " + hbold(name) + f"! Я бот предназначенный для постинга новых курсов с сайта {hlink(SITE_LINK, 'udemy')}\n"
                                                "Если хочешь получать уведомления от меня подпишись!\n"
                                                "on - подписаться\noff - отписаться", reply_markup=keyboard)


@dp.message_handler(Text(equals="on"))
async def on(msg: types.Message):
    user_id = str(msg.from_user.id)
    name = msg.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
    if cursor.fetchone() is None:
        db.execute(f"INSERT INTO users VALUES(?,?)", (user_id, name))
        db.commit()
        await bot.send_message(user_id, name + ", вы подписаны! Рассылка с сайта " + hlink(
            'Udemy', SITE_LINK) + " активирована")
        await bot.send_message(ADMIN_ID,
                               f"Привет " + hbold(ADMIN_NAME) + "! Хотел сообшить что новый пользователь " + name +
                               " присоеденился "
                               "ко мне!")
    else:
        await bot.send_message(user_id, "Вы уже подписаны!")


@dp.message_handler(Text(equals="off"))
async def off(msg: types.Message):
    user_id = str(msg.from_user.id)
    name = msg.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
    if cursor.fetchone() is not None:
        cursor.execute(f"DELETE FROM users WHERE id = '{user_id}'")
        await bot.send_message(user_id, "Вы отписались от рассылки")
        await bot.send_message(ADMIN_ID, f"Привет " + hbold(ADMIN_NAME) + "! Хотел сообшить что пользователь " + name +" отписался от меня(")
    else:
        await bot.send_message(user_id, "Вы и так та не подписаны)(on - подписаться)")


# parser
async def news_every_minute():
    while True:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285"
        }
        req = requests.get("https://coursevania.com/courses/", headers=headers)
        soup = BeautifulSoup(req.text, "lxml")
        course = soup.find(class_ = "stm_lms_courses__single stm_lms_courses__single_animation no-sale style_1")
        print("course: " + course.find(class_ = "stm_lms_courses__single--title").find("h5").text)
        try:
            print("check_car: " + check_course.find(class_ = "stm_lms_courses__single--title").find("h5").text)
        except:
            check_course = course
        if check_course.find(class_ = "stm_lms_courses__single--title").find("h5").text != course.find(class_ = "stm_lms_courses__single--title").find("h5").text:
            course_price = course.find(class_ = "stm_lms_courses__single--price heading_font").find("strong").text
            course_link = course.find(class_ = "stm_lms_courses__single--title").find("a").get("href")
            soup = BeautifulSoup(requests.get(course_link, headers = headers).text, "lxml")
            udemy_course_link = soup.find(class_ = "stm-lms-buy-buttons").find("a").get("href")
            course_name = soup.find(class_ = "stm_lms_course__title").text
            if course_price == "Free":
                time_for = "Текущая цена доступка на 2 дня"
                for user_id in cursor.execute("SELECT id FROM  users"):
                    user_id = ''.join(sym for sym in user_id)
                    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={user_id}&text="
                                 f"Название: {course_name}\nЦена: {course_price}\n{time_for}\nСсылка: {udemy_course_link}")
                check_course = course
            else:
                for user_id in cursor.execute("SELECT id FROM  users"):
                    user_id = ''.join(sym for sym in user_id)
                    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={user_id}&text="
                                 f"Название: {course_name}\nЦена: {course_price}\nСсылка: {udemy_course_link}")
                check_course = course
        await asyncio.sleep(3)


async def get_started(dp):
    sub_buttons = ["on", "off"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*sub_buttons)
    for value in cursor.execute("SELECT id FROM users"):
        value = ''.join(c for c in value)
        await bot.send_message(value, "я запущен!", reply_markup=keyboard)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp, on_startup=get_started)
