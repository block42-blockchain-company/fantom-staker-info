from web3 import Web3


class Web3Client:
    def __init__(self):
        self.__web3 = Web3(Web3.HTTPProvider("https://rpc.fantom.b42.tech"))

    def instance(self):
        return self.__web3

    def getBalance(self, address):
        return self.instance().eth.getBalance(self.instance().toChecksumAddress(address)) / 1e18
