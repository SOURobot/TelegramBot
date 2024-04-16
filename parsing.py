import pprint
import json
import requests
from bs4 import BeautifulSoup


TOKEN = "335150ec234b41d5d5501e72eaa709c5"


def main_func(filters):
    ending, other_keys = create_link(filters)
    curr_html = get_html(ending)
    pprint.pprint(curr_html)


def open_cities():
    data = []
    with open("data/base.txt", "r") as c:
        cities = c.read().split("\n")
        for line in cities:
            data.extend(line.split(", "))
        c.close()
    return data


def create_link(filters):
    # unique=false&sorting=price&direct=false&currency=rub&limit=30&page=1&one_way=true&token=РазместитеЗдесьВашТокен

    ending = ""

    ending += "origin=" + {"*": "MOW", "Внуково": "VKO", "Домодедово": "DME", "Шереметьево": "SVO"}[filters["airport"]]
    ending += f"&unique=true&sorting=price&direct=true&limit={filters['amount']}&one_way=true&token={TOKEN}"

    other_keys = {"time": filters['time'], "duration": filters['duration'], "cost": filters['cost']}

    return ending, other_keys


def get_html(ending):
    # st_accept = "text/html"
    # st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"
    # headers = {"Accept": st_accept, "User-Agent": st_useragent}

    link = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?{ending}"
    req = requests.get(link)
    src = req.json()
    return src


def get_info(code):
    airline = code["airline"]
    city = code["destination"]
    duration = code["duration"]


main_func({
    "airport": "Внуково", "amount": 5, "time": "после 18", "duration": 300, "cost": 3000
})