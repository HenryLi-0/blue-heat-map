from settings import *
import requests, os, time, math, sqlite3

INT_LIMIT = (2**31)-1
SMALLINT_LIMIT = (2**15)-1

def clamp(value:int, maxV:int):
    return max(-maxV, min(value, maxV))

class Backend:
    def __init__(self):
        pass

class Debug:
    def __init__(self):
        self.initTime = round(time.time())
        self.path = os.path.join("app", "storage", "debug-{}.txt".format(round(time.time())))
        with open(self.path, "w") as f:
            f.write("")
            f.close()
    def log(self, name, error, text):
        data = "{:8} | {} | {:20} | {}".format(
            round((time.time() - self.initTime())*1000)/1000,
            "X" if error else " ",
            name,
            text
        )
        with open(self.path, "a") as f:
            f.write(data)
            f.close()

class SessionWriter:
    def __init__(self, uuid:str, debug:Debug):
        self.initTime = round(time.time())
        self.uuid = str(uuid)
        self.debug = debug
        self.lastCommit = 0

        os.makedirs(os.path.join("app", "storage", self.uuid), exist_ok=True)
        self.path = os.path.join("app", "storage", self.uuid, "{}.db".format(self.initTime))

        with open(self.path, "w") as f:
            f.write("")
            f.close()
        self.db = sqlite3.connect(self.path)
        self.c = self.db.cursor()

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS player_activity (
            timestamp SMALLINT NOT NULL,
            x INTEGER NOT NULL,
            y SMALLINT NOT NULL,
            z INTEGER NOT NULL,
            f BOOLEAN NOT NULL,
            PRIMARY KEY (timestamp)
        );
        ''')
        self.debug.log("SessionWriter_" + self.uuid[0:6], False, "created")

    def data(self, timestamp:int, x:int, y:int, z:int, f:bool):
        try:
            self.c.execute('''
            INSERT INTO player_activity (timestamp, x, y, z, f)
            VALUES (?, ?, ?, ?, ?)
            ''', (clamp(round(timestamp-self.initTime), SMALLINT_LIMIT),
                clamp(x, INT_LIMIT),
                clamp(y, SMALLINT_LIMIT),
                clamp(z, INT_LIMIT),
                f
            ))
            self.lastCommit += 1
        except Exception as e:
            self.debug.log("SessionWriter_" + self.uuid[0:6], True, "log {}".format(e))
        if self.lastCommit >=  LOGS_UNTIL_COMMIT:
            try:
                self.db.commit()
                self.lastCommit = 0
            except Exception as e:
                self.debug.log("SessionWriter_" + self.uuid[0:6], True, "commit {}".format(e))

    def close(self):
        success = False
        attempts = 0
        while not(success) and attempts <= MAX_SAVE_ATTEMPTS:
            try:
                self.db.commit()
                success = True
            except Exception as e:
                self.debug.log("SessionWriter_" + self.uuid[0:6], True, "close {}".format(e))
                time.sleep(0.1)
                attempts += 1
        return success
        