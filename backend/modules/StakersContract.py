import json

from datetime import datetime


class StakersContract:
    def __init__(self, fantomApi):
        self.__address = "0xfc00face00000000000000000000000000000000"
        self.__instance = fantomApi.web3().eth.contract(
            address=fantomApi.web3().toChecksumAddress(self.__address),
            abi=json.loads(open("abi/Stakers.abi.json", "r").read())
        )

    def instance(self):
        return self.__instance

    def getAddress(self):
        return self.__address

    def getEvents(self, eventName, options=None):
        args = {} if options is None else options
        return self.__instance.events[eventName].createFilter(fromBlock=0, toBlock="latest", argument_filters=args).get_all_entries()

    def getValidatorCount(self):
        return self.__instance.functions.stakersNum().call()

    def getValidationStake(self, validatorId):
        return self.__instance.functions.stakers(validatorId).call()

    def getDelegations(self, address):
        return self.__instance.functions.delegations(address).call()

    def getCurrentSealedEpochId(self):
        return self.__instance.functions.currentSealedEpoch().call()

    def getEpochSnapshot(self, epochId):
        return self.__instance.functions.epochSnapshots(epochId).call()

    def getEpochValidator(self, epochId, validatorId):
        return self.__instance.functions.epochValidator(epochId, validatorId).call()

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