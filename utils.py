from bs4 import BeautifulSoup
import telebot
import datetime
from config import TELEGRAM_TOKEN_BOT, USER_CHAT_ID


def get_bloks_of_page(bs_page: BeautifulSoup):
    bloks = bs_page.find_all("div", class_= "iva-item-content-rejJg")
    return bloks


def get_general_data(bs_one_block):
    """Возвращает 1-Ссылку, 2-Название"""
    one = bs_one_block.find_all("a", class_="iva-item-sliderLink-uLz1v")[0]
    yield one["href"]
    yield one["title"]


def send_message(txt: str) -> None:
    """ 
    Функция для отправки сообщения в Telegram бота
    """
    bot = telebot.TeleBot(str(TELEGRAM_TOKEN_BOT))
    bot.send_message(str(USER_CHAT_ID),txt)


def check_write_links(url_link: str) -> bool:
    """
    Функция логгер, создаёт файл linx.txt в директорию 
    от куда было запущено приложение, и записывает в файл время и ссылку на
    подходящий товар по параметраметрам.
    """
    #можно усовершенствовать, создать БД либо SQlite и записывать в неё
    #ещё надо разобраться с местом появления файла или бд, что бы 
    #создавалось только в корневой папке, а не в месте от куда запускается приложение
    #было бы здорово интегрироваться с googlesheets

    with open("links.txt") as file:
        text = file.read()

    links = str(text).split("\n")

    dat = datetime.datetime.now()

    if url_link in links:
        return False

    else:
        with open("links.txt", "a") as z:
            z.write(f"{dat}\n")


        with open("links.txt", "a") as t:
            t.write(f"{url_link}\n")
        return True


