with open("../data/base.txt", "r") as c:
    cities = c.read().split("\n")
    data = []
    for line in cities:
        data.extend(line.split(", "))
    data.sort()
    c.close()


with open("../data/cities.txt", "w") as c:
    stage = 0
    while stage != 4:
        row = ""
        for i in range(24 * stage, min(len(data), 24 + 24 * stage)):
            if row:
                row += ", " + data[i]
            else:
                row += data[i]
        if stage:
            c.write("\n")
            c.write(row)
        else:
            c.write(row)

        stage += 1