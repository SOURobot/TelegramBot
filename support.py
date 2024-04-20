import sqlite3

with open("../data/base.txt", "r", encoding="utf-8") as c:
    cities = str(c.read())[1:-1].split("}, {")
    data = []
    for line in cities:
        data.append(line.split(", "))
    data.sort()
    c.close()

    connection = sqlite3.connect('../SQL_database/AIR')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Cities')
    for city in data:
        print(city)
        code, name = city[0], city[1].lower().capitalize()
        cursor.execute('INSERT INTO Cities (code, name) VALUES (?, ?)', (code, name))
        connection.commit()
    connection.close()


# with open("../data/cities.txt", "w") as c:
#     stage = 0
#     while stage != 4:
#         row = ""
#         for i in range(24 * stage, min(len(data), 24 + 24 * stage)):
#             if row:
#                 row += ", " + data[i]
#             else:
#                 row += data[i]
#         if stage:
#             c.write("\n")
#             c.write(row)
#         else:
#             c.write(row)
#
#         stage += 1