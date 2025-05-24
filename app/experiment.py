import sqlite3
import os
import random

for ie in range(10):
    testDB = os.path.join("app", "storage","experiment{}.db".format(ie))
    with open(testDB, "w") as f:
        f.write("")
        f.close()
    db = sqlite3.connect(testDB)
    c = db.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS player_activity (
        timestamp TEXT NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        z INTEGER NOT NULL,
        PRIMARY KEY (timestamp)
    );
    ''')

    def log(time, x, y, z):
        c.execute('''
        INSERT INTO player_activity (timestamp, x, y, z)
        VALUES (?, ?, ?, ?)
        ''', (time, x, y, z))

    r = lambda: str(random.randint(0,1000000))

    for i in range(60*60):
        log(i, r(), r(), r())
        if i % 60 == 0: print("write {}".format(i))
    db.commit()


    # c.execute('SELECT * FROM player_activity ORDER BY timestamp')
    # rows = c.fetchall()

    # # rows?
    # for row in rows:
    #     print(row)
    db.close()