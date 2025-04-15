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

class LogWritingUtils:
    @staticmethod
    def toBinary(baseTen, forceMinSize = False):
        return bin(baseTen)[2:].rjust(forceMinSize, "0") if forceMinSize else bin(baseTen)[2:]
    @staticmethod
    def packWithHeader(data):
        return LogWritingUtils.toBinary(len(data), 5) + data
    @staticmethod
    def packStartingBlock(x, y, z):
        return "00000" + str((abs(x) == x) + 0) + LogWritingUtils.toBinary(abs(x), 23) + str((abs(y) == y) + 0) + LogWritingUtils.toBinary(abs(y), 7) + str((abs(z) == z) + 0) + LogWritingUtils.toBinary(abs(z), 23)
    @staticmethod
    def packLog(t, x, y, z, forceT = False):
        concat = ""
        if t != 1 or forceT:
            concat += LogWritingUtils.packWithHeader("00" + LogWritingUtils.toBinary(data))
        for index, data in enumerate([x, y, z]):
            concat += LogWritingUtils.packWithHeader(LogWritingUtils.toBinary(index + 1, 2) + str((abs(data) == data) + 0) + LogWritingUtils.toBinary(abs(data)))
        return concat
    @staticmethod
    def packSafety():
        return "00000000"

    
class LogWriter:
    def __init__(self, playerUUID:str):
        self.initLogTime = time.time()
        self.playerUUID = playerUUID
        self.dataIndex = None

        self.lastLogTime = time.time()
        self.lastLog = {}
        self.delay = self.lastLogTime - self.initLogTime

        self.latestData = None
        self.queue = []
        self.scanID()

        # init block
        
        
        # self.latestData
    
    def scanID(self):
        for i, group in enumerate(Network.data["players"]):
            if group["uuid"] == self.playerUUID:
                self.latestData = group
                self.dataIndex = i
                break
        if self.dataIndex == None:
            print("IndexError: No UUID {} found in Network data!".format(self.playerUUID))

    def log(self):
        '''Logs the file if more time since the last update has passed than the frequency. Meant to be called repeatedly.'''
        if (time.time()-self.lastLogTime) > FREQUENCY:
            if not Network.data["players"][self.dataIndex]["uuid"] == self.playerUUID:
                print("Player UUID index update detected! Updating...")
                self.scanID()
            if Network.data["players"][self.dataIndex]["uuid"] == self.playerUUID:
                self.lastLog = Network.data["players"][self.dataIndex]

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