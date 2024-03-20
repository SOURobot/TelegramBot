import requests


def main_func(filters):
    cities = open_cities()
    for city in cities:
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
    ending = ""

    ending += {"*": "MOW", "Внуково": "VKO", "Домодедово": "DME", "Шереметьево": "SVO"}[filters['airport']]
    ending += city
    ending += str(filters['passengers'])

    other_keys = {"time": filters['time'], "duration": filters['duration'], "cost": filters['cost']}

    return ending, other_keys


def get_html(ending):
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"
    headers = {"Accept": st_accept, "User-Agent": st_useragent}

    link = f"https://www.aviasales.ru/?params={ending}"
    print(link)
    req = requests.get(link, headers)
    src = req.text
    return src