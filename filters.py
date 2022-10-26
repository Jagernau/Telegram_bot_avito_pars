
from bs4 import BeautifulSoup
from non_except import exceptions_time, exceptions_descipt
import re

def filter_from_time(bs_block: BeautifulSoup):
    time = bs_block.find_all("div", class_="date-text-KmWDf")[0].contents[0]
    t = time.split(" ")[1]
    if t in exceptions_time:
        return False
    else:
        return True

def filter_from_non_text(bs_block: BeautifulSoup):
    all_text = str(bs_block)
    for y in exceptions_descipt:
        compi = re.compile(rf".{y}.").match(all_text)
        if compi:
            return False
        else:
            return True


def filter_price(bs_block: BeautifulSoup):
    """Фильтрует цену в блоке"""
    one = bs_block.find_all("span", class_="price-price-JP7qe")[0].contents[1]["content"]
    
    if int(one) > 150000:
        return False
    if int(one) < 80000:
        return False

    else:
        return True

