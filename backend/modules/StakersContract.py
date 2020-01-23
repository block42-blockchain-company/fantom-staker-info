import json

from datetime import datetime


class StakersContract:
    def __init__(self, web3):
        self.__instance = web3.eth.contract(
            address=web3.toChecksumAddress("0xfc00face00000000000000000000000000000000"),
            abi=json.loads(open("interfaces/Stakers.abi.json", "r").read())
        )

    def getValidatorCount(self):
        return self.__instance.functions.stakersNum().call()

    def getValidatorInfo(self, validatorId):
        return self.__instance.functions.stakers(validatorId).call()

    def getDelegations(self, address):
        return self.__instance.functions.delegations(address).call()

    def getCurrentSealedEpochId(self):
        return self.__instance.functions.currentSealedEpoch().call()

    def getEpochSnapshot(self, epochId):
        return self.__instance.functions.epochSnapshots(epochId).call()

    def getRoi(self):
        currentSealedEpoch = self.__instance.functions.currentSealedEpoch().call()
        epochSnapshot = self.__instance.functions.epochSnapshots(currentSealedEpoch).call()

        epochBaseRewardPerSecond = epochSnapshot[5] / 1e18
        epochStakeTotalAmount = epochSnapshot[6] / 1e18
        epochDelegationsTotalAmount = epochSnapshot[7] / 1e18

        oneYearInSeconds = 60 * 60 * 24 * 365

        return (epochBaseRewardPerSecond / (epochStakeTotalAmount + epochDelegationsTotalAmount)) * oneYearInSeconds * 0.85  # 15% validator fee

    def getRewardUnlockPercentage(self):
        unbondingStartDate = self.__instance.functions.unbondingStartDate().call()
        unbondingPeriod = self.__instance.functions.unbondingPeriod().call()

        passedTime = int(datetime.now().timestamp() - unbondingStartDate)
        passedPercent = passedTime / unbondingPeriod

        return 0.8 if passedPercent >= 0.8 else 0.8 - passedPercent

    def getRewardUnlockDate(self):
        unbondingStartDate = self.__instance.functions.unbondingStartDate().call()
        unbondingUnlockPeriod = self.__instance.functions.unbondingUnlockPeriod().call()

        return unbondingStartDate + unbondingUnlockPeriod

    def getTotalSupply(self):
        currentSealedEpoch = self.__instance.functions.currentSealedEpoch().call()
        epochSnapshot = self.__instance.functions.epochSnapshots(currentSealedEpoch).call()

        return epochSnapshot[8] / 1e18