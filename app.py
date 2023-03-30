from bs4 import BeautifulSoup
from requests import get, ConnectionError, ConnectTimeout, Timeout, HTTPError
from utils import get_blocks_of_page, send_message,  check_write_links
from filters import filter_from_time, filter_price
import time
import random
import argparse
from config import SITY

parser = argparse.ArgumentParser(description="Name of product")
parser.add_argument("name", type=str)
arg = parser.parse_args()
product = arg.name
ur = f"https://www.avito.ru/{SITY}?q={product}"

for i in range(1, random.randint(10,19)):
    time.sleep(random.randint(2, 7))
    url = str(ur + f"&p={i}") # проход по пагинации,
                              # i- номер страницы, на странице
                              # 10 товаров.
    try:
        response = get(url) #GET запрос requests
        assert response.status_code == 200, AssertionError
    except(ConnectionError, ConnectTimeout, Timeout, HTTPError):
        raise SystemExit(1)
    except AssertionError:
        raise SystemExit(1)
    else:
        page = response.content.decode("utf-8") #Переводит русские символы
        #Форматирует страницу в формат BeautifulSoup
        bs_page = BeautifulSoup(str(page), "html.parser")
        #Разбивает страницу на блоки- товары, как list
        products_blocks = get_blocks_of_page(bs_page)
        for block in products_blocks:
            
            # фильтрация по времени
            if not filter_from_time(block):
                continue
            # фильтрация по цене
            if not filter_price(block):
                continue
            
            found_link = block.findAll('a', href=True)[0]["href"]
            link:str = f"https://www.avito.ru{str(found_link)}"
            
            # проверяет на индивидуальность
            if check_write_links(link) == False:
                continue

            text:str = f"\nСсылка:  {link}\n"
            
            time.sleep(random.randint(1, 5))
            send_message(text)
