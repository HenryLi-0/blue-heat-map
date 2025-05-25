# import sqlite3
# import os
# import random

# for ie in range(10):
#     testDB = os.path.join("app", "storage","experiment{}.db".format(ie))
#     with open(testDB, "w") as f:
#         f.write("")
#         f.close()
#     db = sqlite3.connect(testDB)
#     c = db.cursor()

#     c.execute('''
#     CREATE TABLE IF NOT EXISTS player_activity (
#         timestamp SMALLINT NOT NULL,
#         x INTEGER NOT NULL,
#         y SMALLINT NOT NULL,
#         z INTEGER NOT NULL,
#         f BOOLEAN NOT NULL,
#         PRIMARY KEY (timestamp)
#     );
#     ''')

#     def log(time, x, y, z, f):
#         c.execute('''
#         INSERT INTO player_activity (timestamp, x, y, z, f)
#         VALUES (?, ?, ?, ?, ?)
#         ''', (time, x, y, z, f))

#     r = lambda: random.randint(0,1000000)

#     for i in range(60*60):
#         log(i, random.randint(-1000000,1000000), random.randint(-1024,1024), random.randint(-1000000,1000000), False)
#         if i % 60 == 0: print("write {}".format(i))
#     db.commit()


#     # c.execute("SELECT * FROM player_activity ORDER BY timestamp")
#     # rows = c.fetchall()

#     # # rows?
#     # for row in rows:
#     #     print(row)
#     db.close()

# from backend import Network
# import time

# while True:
#     Network.tick()
#     print(Network.getUUID("some uuid"))
#     time.sleep(1)




# from backendLog import BackendLog
# import time
# backend = BackendLog()
# lastUpdate = 0
# while True:
#     if time.time()-lastUpdate > 1:
#         backend.tick()
#         lastUpdate = time.time()




# import sqlite3, os
# db = sqlite3.connect(os.path.join("app", "storage", "uuid", "log"))
# c = db.cursor()
# c.execute('SELECT * FROM player_activity ORDER BY timestamp')
# rows = c.fetchall()
# for row in rows:
#     print(row)
# db.close()


import os
from backendRead import Datalog
reader = Datalog(os.path.join("app", "storage", "uuid","log"))
data = reader.read()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import colorsys

rgbDecToHex = lambda rgb: "#" + "".join(["{:02}".format(hex(round(item*255))[2:]).replace(" ", "0") for item in rgb])

xs = [p[1] for p in data]
ys = [p[2] for p in data]
zs = [p[3] for p in data]
colors = [rgbDecToHex(colorsys.hsv_to_rgb(i/len(data), 1, 1)) for i in range(len(data))]

plot = plt.figure()
ax = plot.add_subplot(111, projection='3d')

# y and z swapped for mc
# s for point size?
ax.scatter(xs, zs, ys, c=colors, s=60)
ax.plot(xs, zs, ys, c="black")

#labels
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')
ax.set_title('3D Point Visualization')

plt.show()
