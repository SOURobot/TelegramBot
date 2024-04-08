import pprint

import requests
from bs4 import BeautifulSoup


TOKEN = "335150ec234b41d5d5501e72eaa709c5"


def main_func(filters):
    cities = open_cities()
    for city in cities[::-1]:
        ending, other_keys = create_link(filters, city)
        curr_html = get_html(ending)
        print(curr_html)
        break


def open_cities():
    data = []
    with open("data/base.txt", "r") as c:
        cities = c.read().split("\n")
        for line in cities:
            data.extend(line.split(", "))
        c.close()
    return data


def create_link(filters, city):
    # unique=false&sorting=price&direct=false&currency=rub&limit=30&page=1&one_way=true&token=РазместитеЗдесьВашТокен

    ending = ""

    ending += "origin=" + {"*": "MOW", "Внуково": "VKO", "Домодедово": "DME", "Шереметьево": "SVO"}[filters["airport"]]
    # ending += "&destination" + city
    ending += f"&unique=true&sorting=price&direct=true&limit=1&one_way=true&token={TOKEN}"

    other_keys = {"time": filters['time'], "duration": filters['duration'], "cost": filters['cost']}

    return ending, other_keys


def get_html(ending):
    # st_accept = "text/html"
    # st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"
    # headers = {"Accept": st_accept, "User-Agent": st_useragent}

    link = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?{ending}"
    req = requests.get(link)
    src = req.text
    return src


def get_info(code):
    soup = BeautifulSoup(code, "lxml")
    data = soup.find_all('span', class_="s__wRhMOEwg2Ub7G1CotYcY")
    print(data)


main_func({
    "airport": "Внуково", "time": "после 18", "duration": 300, "cost": 3000
})