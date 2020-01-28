import json


class StakerInfoContract:
    def __init__(self, web3):
        self.__instance = web3.instance().eth.contract(
            address=web3.instance().toChecksumAddress("0x92ffad75b8a942d149621a39502cdd8ad1dd57b4"),
            abi=json.loads(open("interfaces/StakerInfo.abi.json", "r").read())
        )

    def getConfigUrl(self, validatorId):
        return self.__instance.functions.stakerInfos(validatorId).call()
