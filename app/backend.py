from settings import *
import requests, os, time

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
    def __init__(self):
        pass
    def tick(self):
        try:
            Network.reponse = requests.get(PLAYERS_JSON)
            Network.status = Network.reponse.status_code
            Network.data = Network.reponse.json()
        except:
            Network.data = {}

class LogWriter:
    def __init__(self, playerUUID:str):
        self.initLog = time.time()
        self.playerUUID = playerUUID
        self.queue = []
        self.lastLog = time.time()
        self.delay = self.lastLog - self.initLog
        self.latestData = None
        self.dataIndex = None

        # init block
        Network.tick()
        
        for i, group in enumerate(Network.data["players"]):
            if group["uuid"] == self.playerUUID:
                self.latestData = group
                self.dataIndex = i    
                break
        if self.dataIndex == None:
            print("IndexError: No UUID {} found in Network data!".format(self.playerUUID))
        
        # self.latestData

        
    def log(self):
        '''Logs the file if more time since the last update has passed than the frequency. Meant to be called repeatedly.'''
        if (time.time()-self.lastLog) > FREQUENCY:
            

            self.lastLog += FREQUENCY
            self.delay = time.time()-self.lastLog
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