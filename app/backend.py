from settings import PLAYERS_JSON
import requests

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

class PlayerSession:
    def __init__(self, UUID=None):
        pass
    def tick(self):
        pass

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
        