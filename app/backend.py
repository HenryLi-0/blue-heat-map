from settings import *
import requests, os, time,math

class BackEnd:
    def __init__(self):
        self.liveSessions = []
        pass
    def tick(self):

        # test for existing players and join/leave
        # update players list
        # process existing players
        # repeat

        for session in self.liveSessions:
            session.tick()

class Network:
    response = ""
    status = 200
    data = {}
    @staticmethod
    def tick():
        try:
            Network.response = requests.get(PLAYERS_JSON)
            Network.status = Network.response.status_code
            Network.data = Network.response.json()
        except:
            Network.data = {}

class DataLog:
    @staticmethod
    def toBinary(baseTen, forceMinSize = False):
        return bin(baseTen)[2:].rjust(forceMinSize, "0") if forceMinSize else bin(baseTen)[2:]

    def __init__(self):
        self.dataLog = []

    def packWithHeader(self, data):
        self.dataLog.append(DataLog.toBinary(len(data), 5) + data)
    def packStartingBlock(self, x, y, z):
        self.dataLog.append("00000" + str((abs(x) == x) + 0) + DataLog.toBinary(abs(x), 23) + str((abs(y) == y) + 0) + DataLog.toBinary(abs(y), 7) + str((abs(z) == z) + 0) + DataLog.toBinary(abs(z), 23))
    def packLog(self, t, x, y, z, forceT = False):
        concat = ""
        if t != 1 or forceT:
            concat += DataLog.packWithHeader("00" + DataLog.toBinary(data))
        for index, data in enumerate([x, y, z]):
            concat += DataLog.packWithHeader(DataLog.toBinary(index + 1, 2) + str((abs(data) == data) + 0) + DataLog.toBinary(abs(data)))
        self.dataLog.append(concat)
    def packSafety(self):
        self.dataLog.append("00000000")

    def save(self):
        # TODO: compress to file
        pass

    
class LogWriter:
    def __init__(self, playerUUID:str):
        self.initLogTime = time.time()
        self.playerUUID = playerUUID
        self.dataIndex = None

        self.lastLogTime = time.time()
        self.delay = self.lastLogTime - self.initLogTime

        self.latestData = None
        self.lastData = self.latestData
        self.dataLog = DataLog()
        self.scanID()

        '''
        log = log into data logs
        data = data from network
        '''

        # init block
        self.dataLog.packStartingBlock(
            round(self.latestData["position"]["x"]),
            round(self.latestData["position"]["y"]),
            round(self.latestData["position"]["z"])
        )
        
        # self.latestData
    
    def scanID(self):
        for i, group in enumerate(Network.data["players"]):
            if group["uuid"] == self.playerUUID:
                self.latestData = group
                self.dataIndex = i
                break
        if self.dataIndex == None:
            print("IndexError: No UUID {} found in Network data!".format(self.playerUUID))
            # TODO: implement automatic log closing

    def log(self):
        '''Logs the file if more time since the last update has passed than the frequency. Meant to be called repeatedly.'''
        if (time.time()-self.lastLogTime) > FREQUENCY:
            if not Network.data["players"][self.dataIndex]["uuid"] == self.playerUUID:
                print("Player UUID index update detected! Updating...")
                self.scanID()
            if Network.data["players"][self.dataIndex]["uuid"] == self.playerUUID:
                self.latestData = Network.data["players"][self.dataIndex]

            self.lastLogTime += FREQUENCY
            self.delay = time.time()-self.lastLogTime
    def getLastLogDelayMS(self):
        '''Returns the delay in the last log in milliseconds (1/1000 seconds).'''
        return round(self.delay*1000)
    def push(self):
        '''Pushes changes to the save file. Fast repeated calls not recommended.'''
        pass



class LogReader:
    def __init__(self, load:str):
        self.data = None
        try:
            extension = load[load.find("."):]
            if extension == ".dat":
                self.data = open(os.path.join(load), "r")
            else: print(f"'{extension}' file extension isn't supported!")
        except: print("Failed to load log!")
    def parse(self):
        pass