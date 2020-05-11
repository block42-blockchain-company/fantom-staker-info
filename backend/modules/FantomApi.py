import requests

from web3 import Web3


class FantomApi:
    def __init__(self):
        self.__url = "https://rpc.fantom.network"
        self.__web3 = Web3(Web3.HTTPProvider(self.__url))

    def web3(self):
        return self.__web3

    def getBalance(self, address):
        return self.web3().eth.getBalance(self.instance().toChecksumAddress(address)) / 1e18

    def getLatestBlockNumber(self):
        return self.web3().eth.blockNumber

    def getBlock(self, height):
        return self.web3().eth.getBlock(height)

    def getTransaction(self, txHash):
        return self.web3().eth.getTransaction(txHash)

    def getTransactionReceipt(self, txHash):
        return self.web3().eth.getTransactionReceipt(txHash)

    def getAllEpochEvents(self, epochId):
        return requests.post(url=self.__url, json={
            "jsonrpc": "2.0",
            "method": "ftm_getHeads",
            "params": [hex(epochId)],
            "id": 1
        }).json()["result"]

    def getEpochEvent(self, eventId):
        response = requests.post(url=self.__url, json={
            "jsonrpc": "2.0",
            "method": "ftm_getEvent",
            "params": [eventId, True],
            "id": 1
        }).json()

        result = None

        try:
            result = response['result']
        except KeyError:
            if 'error' in response:
                print(response["error"]["message"])

        return result
