import random
import sqlite3

import requests


TOKEN = "335150ec234b41d5d5501e72eaa709c5"


def main_func(filters):
    ending, other_keys = create_link(filters)
    curr_html = get_html(ending)
    pull_info(curr_html)
    results = get_info(other_keys)
    out = random.sample(results, min(other_keys["amount"], len(results)))
    return format_out(out)


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
    other_keys = {"amount": filters['amount'],
                  "time": "> " + str(int(hours[1]) * 60) if hours[0] == "после" else "< " + str(int(hours[1]) * 60),
                  "duration": filters['duration'],
                  "cost": filters['cost']}

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
        dep_time = (int(var["departure_at"][11:13]) + 3) * 60 + int(var["departure_at"][14:16])
        dep_date = ".".join(var["departure_at"][:10].split("-")[::-1])
        duration = var["duration"]
        price = var["price"]
        cursor.execute('INSERT INTO InStream (city, airline, dep_time, dep_date, duration, price) VALUES (?, ?, ?, ?, ?, ?)',
                       (city, airline, dep_time, dep_date, duration, price))
        connection.commit()
    connection.close()


def get_info(filters):
    connection = sqlite3.connect('SQL_database/AIR')
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT city, airline, dep_time, dep_date, duration, price
    FROM InStream
    WHERE dep_time {filters["time"]} and duration <= ? and price <= ?
    ''', (filters["duration"], filters["cost"]))
    results = cursor.fetchall()
    results = list(set(results))
    return results


def format_out(out):
    if not out:
        return "Похоже, по вашему запросу ничего не найдено."
    text = ""
    for ticket in out:
        text += "Город 🏙: " + ticket[0] + "\n"
        text += "Авиакомпания ✈: " + ticket[1] + "\n"
        text += "Дата и время 📆: " + ticket[3] + " " + str(ticket[2] // 60)+ ":" + str(ticket[2] % 60) + "\n"
        text += "Продолжительность ⌚: " + str(ticket[4]) + " минут\n"
        text += "Стоимость билета 💵: " + str(ticket[5]) + " рублей\n"
        text += "\n"
    return text[:-4]


main_func({
    "airport": "Шереметьево", "amount": 5, "time": "до 23", "duration": 300, "cost": 5000
})