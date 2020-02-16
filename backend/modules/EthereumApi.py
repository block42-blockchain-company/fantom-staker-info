import os
import requests


class EthereumApi:
    def __init__(self):
        self.__url = os.environ["ETHEREUM_ENDPOINT_URL"]

    def getLatestBlockHeight(self):
        return int(requests.post(self.__url, json={
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }).json()["result"], 16)

    def getTransfers(self, fromBlock, toBlock):
        return requests.post(self.__url, json={
            "jsonrpc": "2.0",
            "method": "eth_getLogs",
            "params": [{
                "address": "0x4e15361fd6b4bb609fa63c81a2be19d873717870",
                "fromBlock": hex(fromBlock),
                "toBlock": hex(toBlock),
                "topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]
            }],
            "id": 1
        }).json()["result"]
