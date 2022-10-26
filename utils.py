from bs4 import BeautifulSoup
import subprocess
import telebot
import datetime
from filters import filter_from_non_text, filter_from_time, filter_price
import lxml

def kil_and_run_tor(url):
    to = subprocess.run(["pidof", "tor"], text=True, capture_output=True)
    val = ["kill", str(to.stdout).strip()]
    subprocess.Popen(val)
    subprocess.run(["sv", "stop", "tor"])
    subprocess.Popen("tor")
    page = subprocess.run(["proxychains4", "curl", f"{url}"], text=True, capture_output=True)

    bs_page = BeautifulSoup(str(page), "lxml")
    bloks = get_bloks_of_page(bs_page)
    for i in bloks:
        
        #фильтр по времени
        if not filter_from_time(i):
            continue
        if not filter_price(i):
            continue
        if not filter_from_non_text(i):
            continue
        
        datas = get_general_data(i)
        href = f"https://www.avito.ru{str(next(datas))}"
        title = str(next(datas))
        
        if write_log_links(href) == False:
            continue

        text = f"\nСсылка:  {href}\nОписание:  {title}\n"

        send_message(text)



def get_bloks_of_page(bs_page: BeautifulSoup):
    bloks = bs_page.find_all("div", class_= "iva-item-content-rejJg")
    return bloks


def get_general_data(bs_one_block):
    """Возвращает 1-Ссылку, 2-Название"""
    one = bs_one_block.find_all("a", class_="iva-item-sliderLink-uLz1v")[0]
    yield one["href"]
    yield one["title"]


def send_message(txt: str):
    token = '00'
    bot =telebot.TeleBot(token)
    chat = 00
    bot.send_message(chat,txt)


def write_log_links(url_link):
    with open("links.txt") as f:
        text = f.read()

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


