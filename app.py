from bs4 import BeautifulSoup
from requests import get, ConnectionError, ConnectTimeout, Timeout, HTTPError
from utils import get_bloks_of_page, send_message,  check_write_links
from filters import filter_from_time, filter_price
import time
import random
import argparse
from config import SITY

parser = argparse.ArgumentParser(description="Name of car")
parser.add_argument("name", type=str)
arg = parser.parse_args()
car = arg.name
ur = f"https://www.avito.ru/{SITY}?q={car}"

for i in range(1, random.randint(10,19)):
    time.sleep(random.randint(2, 7))
    url = str(ur + f"&p={i}") # проход по пагинации,
                              # i- номер страницы, на странице
                              # 10 товаров.

    try:
        resp = get(url)
        assert resp.status_code == 200, AssertionError
    except(ConnectionError, ConnectTimeout, Timeout, HTTPError):
        raise SystemExit(1)
    except AssertionError:
        raise SystemExit(1)
    else:
        page = resp.content.decode("utf-8")
        bs_page = BeautifulSoup(str(page), "html.parser")
        bloks = get_bloks_of_page(bs_page)
        for i in bloks:
            
            # фильтрация по времени
            if not filter_from_time(i):
                continue
            # фильтрация по цене
            if not filter_price(i):
                continue
            
            datas = i.findAll('a', href=True)[0]["href"]
            href = f"https://www.avito.ru{str(datas)}"
            
            # проверяет на индивидуальность
            if check_write_links(href) == False:
                continue

            text = f"\nСсылка:  {href}\n"
            
            time.sleep(random.randint(1, 5))
            send_message(text)
