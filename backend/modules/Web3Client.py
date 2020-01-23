from web3 import Web3


class Web3Client:
    def __init__(self):
        self.__web3 = Web3(Web3.HTTPProvider("https://rpc.fantom.network"))

    def instance(self):
        return self.__web3
