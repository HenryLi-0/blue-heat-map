import sqlite3, os

class Datalog:
    def __init__(self, path):
        self.path = path
        try:
            with open(self.path, "r") as f:
                f.close()
            self.db = sqlite3.connect(self.path)
            self.c = self.db.cursor()
        except:
            print("Failed to open datalog {}!".format(self.path))
    def read(self):
        self.c.execute("SELECT * FROM player_activity ORDER BY timestamp")
        rows = self.c.fetchall()
        return rows



class BackendRead:
    def __init__(self):
        pass

