import pprint
import json
import sqlite3

import requests
from bs4 import BeautifulSoup


TOKEN = "335150ec234b41d5d5501e72eaa709c5"


def main_func(filters):
    ending, other_keys = create_link(filters)
    curr_html = get_html(ending)
    pull_info(curr_html)
    get_info(other_keys)


def open_cities():
    data = []
    with open("data/base.txt", "r") as c:
        cities = c.read().split("\n")
        for line in cities:
            data.extend(line.split(", "))
        c.close()
    return data


def create_link(filters):
    ending = ""

    ending += "origin=" + {"*": "MOW", "Внуково": "VKO", "Домодедово": "DME", "Шереметьево": "SVO"}[filters["airport"]]
    ending += f"&unique=true&sorting=price&direct=true&limit=93&one_way=true&token={TOKEN}"

    hours = filters['time'].split()
    other_keys = {"amount": filters['amount'], "time": "> " + hours[1] if hours[0] == "после" else "< " + hours[1], "duration": filters['duration'], "cost": filters['cost']}

    return ending, other_keys


def get_html(ending):
    link = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?{ending}"
    req = requests.get(link)
    src = req.json()
    return src


def pull_info(code):
    connection = sqlite3.connect('SQL_database/AIR')
    cursor = connection.cursor()
    all_cities = code["data"]
    for var in all_cities:
        city = var["destination"]
        airline = var["airline"]
        departure = str(int(var["departure_at"][11:13]) + 3) + ":00 " + ".".join(var["departure_at"][:10].split("-")[::-1])
        duration = var["duration"]
        price = var["price"]
        cursor.execute('INSERT INTO InStream (city, airline, departure, duration, price) VALUES (?, ?, ?, ?, ?)',
                       (city, airline, departure, duration, price))
        connection.commit()
    connection.close()


def get_info(filters):
    connection = sqlite3.connect('SQL_database/AIR')
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT city, airline, departure, duration, price
    FROM InStream
    WHERE departure {filters["time"]} and duration <= ? and price <= ?
    ''', (filters["duration"], filters["cost"]))
    results = cursor.fetchall()
    results = list(set(results))
    for i in results:
        print(i)


main_func({
    "airport": "Внуково", "amount": 5, "time": "до 23", "duration": 300, "cost": 5000
})