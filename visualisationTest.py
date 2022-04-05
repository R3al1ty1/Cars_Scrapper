from main import connectionInit

import numpy as np
import matplotlib.pyplot as plt


con = connectionInit()

#data = con.customSelect("SELECT * FROM main.ads WHERE \"name\" = 'BMW 3-Series' AND \"url\" LIKE '%moscow%'")
data = con.customSelect("SELECT * FROM main.ads")

values = {}
for car in data:
    if str(car[1]) in values:
        values[str(car[1])] += 1
    else:
        values[str(car[1])] = 1
x = []
y = []
for value in values.keys():
    x.append(int(value))
    y.append(values[value])

plt.bar(x, y)

plt.show()