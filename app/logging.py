from settings import *
import requests, os, time, sqlite3
from utils import *

INT_LIMIT = (2**31)-1
SMALLINT_LIMIT = (2**15)-1

class Network:
    response = ""
    status = 0
    data = {}
    timestamp = 0
    @staticmethod
    def tick():
        try:
            Network.response = requests.get(PLAYERS_JSON)
            Network.status = Network.response.status_code
            Network.data = Network.response.json()
            Network.timestamp = time.time()
        except Exception as e:
            Network.data = {}
            Debug.get().log("Network", True, "get {}".format(e))
    @staticmethod
    def getAllUUID():
        uuids = []
        for playerdata in Network.data["players"]:
            uuids.append(playerdata["uuid"])
        return uuids
    @staticmethod
    def getUUID(uuid):
        for playerdata in Network.data["players"]:
            if playerdata["uuid"] == uuid:
                return playerdata
        return None

class SessionWriter:
    def __init__(self, uuid:str):
        self.initTime = round(time.time())
        self.uuid = str(uuid)
        self.debug = Debug.get()
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
                clamp(roundf(x, 1), INT_LIMIT),
                clamp(roundf(y, 1), SMALLINT_LIMIT),
                clamp(roundf(z, 1), INT_LIMIT),
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
                self.db.close()
                success = True
            except Exception as e:
                self.debug.log("SessionWriter_" + self.uuid[0:6], True, "close {}".format(e))
                time.sleep(0.1)
                attempts += 1
        return success

class Logging:
    def __init__(self):
        self.debug = Debug.get()
        Network.tick()
        self.writers:dict[str,SessionWriter] = {}
        for uuid in Network.getAllUUID():
            self.writers[uuid] = SessionWriter(uuid)
        self.tick()
        self.debug.log("Backend", False, "init success")
    
    def tick(self):
        Network.tick()
        # update for active writers
        current = list(self.writers.keys())
        actual = Network.getAllUUID()
        for uuid in actual:
            if not(uuid in current):
                self.writers[uuid] = SessionWriter(uuid)
        for uuid in current:
            if not(uuid in actual):
                if self.writers[uuid].close():
                    self.writers.pop(uuid)
        # tick all writers
        for uuid in actual:
            data = Network.getUUID(uuid)
            self.writers[uuid].data(
                Network.timestamp,
                data["position"]["x"],
                data["position"]["y"],
                data["position"]["z"],
                data["foreign"]
            )