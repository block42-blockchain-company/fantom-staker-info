import json


class StakerInfoContract:
    def __init__(self, fantomApi):
        self.__instance = fantomApi.web3().eth.contract(
            address=fantomApi.web3().toChecksumAddress("0x92ffad75b8a942d149621a39502cdd8ad1dd57b4"),
            abi=json.loads(open("abi/StakerInfo.abi.json", "r").read())
        )

    def getConfigUrl(self, validatorId):
        return self.__instance.functions.stakerInfos(validatorId).call()
