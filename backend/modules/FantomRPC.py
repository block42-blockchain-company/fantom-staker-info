import requests


class FantomRPC:
    def __init__(self):
        self.__rpc = "https://rpc.fantom.b42.tech"

    def getAllEpochEvents(self, epochId):
        return requests.post(url=self.__rpc, json={
            "jsonrpc": "2.0",
            "method": "ftm_getHeads",
            "params": [hex(epochId)],
            "id": 1
        }).json()["result"]

    def getEpochEvent(self, eventId):
        return requests.post(url=self.__rpc, json={
            "jsonrpc": "2.0",
            "method": "ftm_getEvent",
            "params": [eventId, True],
            "id": 1
        }).json()["result"]
