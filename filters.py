from bs4 import BeautifulSoup
from non_except import exceptions_time, exceptions_descipt
import re
from config import HIGHEST_PRICE, LOWER_PRICE

def filter_from_time(bs_block: BeautifulSoup) -> bool:
    """
    Функция проверяет есть ли в блоке товара недопустимыое время, возвращает 
    True, если нет недопустимого слова.
    """
    date_from_poduct = bs_block.find_all("div", class_="date-text-KmWDf")[0].contents[0]
    date = date_from_poduct.split(" ")[1]
    if date in exceptions_time:
        return False
    else:
        return True


# def filter_from_non_text(bs_block: BeautifulSoup) -> bool:
#     all_text = str(bs_block)
#     for y in exceptions_descipt:
#         compi = re.compile(rf".{y}.").match(all_text)
#         if compi:
#             return False
#         else:
#             return True
#

def filter_price(bs_block: BeautifulSoup) -> bool:
    """
    Функция фильтрует цену, если цена продукта
    находится между LOWER_PRICE и HIGHEST_PRICE, возвращает True
    """
    price = bs_block.find_all("span", class_="price-price-JP7qe")[0].contents[1]["content"]
    
    if int(price) > int(HIGHEST_PRICE):
        return False
    if int(price) < int(LOWER_PRICE):
        return False

    else:
        return True

