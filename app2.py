from bs4 import BeautifulSoup
from requests import get, ConnectionError, ConnectTimeout, Timeout, HTTPError
import lxml
from utils import get_bloks_of_page, send_message, get_general_data, write_log_links
from filters import filter_from_time, filter_from_non_text, filter_price
import time
import random
for i in range(1,15):
    time.sleep(random.randint(3, 20))
    url = "https://www.avito.ru/nizhniy_novgorod?q=lada&p={i}"

    try:
        resp = get(url)
        assert resp.status_code == 200, AssertionError("Они меня блокируют")
    except(ConnectionError, ConnectTimeout, Timeout, HTTPError):
        break
    except AssertionError:
        break
    else:
        page = resp.content.decode("utf-8")
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
 

            

