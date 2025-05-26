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
#         lastUpdate = time.time()
#         start = time.time()
#         backend.tick()
#         end = time.time()
#         print("time taken {}s".format(end-start))




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
import matplotlib.pyplot as plt
import colorsys

logs = [("uuid", "start",   "red"),
        ("uuid", "start", "green"),
        ("uuid", "start",  "blue")]
startTime = 0
endTime = 0 + 100
deltaTime = endTime - startTime

plot = plt.figure()
subplot = plot.add_subplot(111, projection='3d')

rgbDecToHex = lambda rgb: "#" + "".join(["{:02}".format(hex(round(max(0, min(item*255, 255))))[2:]).replace(" ", "0") for item in rgb])

for i, data in enumerate(logs):
    
    reader = Datalog(os.path.join("app", "storage", data[0], str(data[1])+".db"))
    fullLogData = reader.read()


    xs = [p[1] for p in fullLogData]
    ys = [p[2] for p in fullLogData]
    zs = [p[3] for p in fullLogData]

    colors = [rgbDecToHex(colorsys.hsv_to_rgb(((data[1]+logData[0])-startTime)/deltaTime, 1, 1)) for logData in fullLogData]


    # y and z swapped for mc
    # s for point size?
    subplot.scatter(xs, zs, ys, c=colors, s=60)
    subplot.plot(xs, zs, ys, c=data[2])

#labels
subplot.set_xlabel('X')
subplot.set_ylabel('Z')
subplot.set_zlabel('Y')
subplot.set_title('3D Point Visualization')

plt.show()
