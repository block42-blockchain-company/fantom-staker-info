import requests

from modules.DefaultConfig import DefaultConfig


class Validators:
    def __init__(self, sfcContract, stakerInfoContract, database):
        self.__sfcContract = sfcContract
        self.__stakerInfoContract = stakerInfoContract
        self.__database = database
        self.__data = []
        self.__totalSupply = self.__sfcContract.getTotalSupply()

    def sync(self, validatorId):
        # Get the config url from smart contract
        configUrl = self.__stakerInfoContract.getConfigUrl(validatorId)

        name = ""
        logoUrl = ""
        website = ""
        contact = ""
        isVerified = False

        try:
            if configUrl is not "":
                requests.packages.urllib3.disable_warnings()
                config = requests.get(configUrl, verify=False).json()

                for key, value in config.items():
                    if key == "name":
                        name = value
                    elif key == "website":
                        website = value
                    elif key == "contact":
                        contact = value
                    elif key == "logoUrl":
                        logoUrl = value

                isVerified = True
            elif DefaultConfig.containsInfoForValidator(validatorId):
                # No config in smart contract found, use bootstrap values
                name = DefaultConfig.getInfoForValidator(validatorId)["name"]
                website = DefaultConfig.getInfoForValidator(validatorId)["website"]
        except Exception:
            pass

        # Get validator info from the sfc smart contract
        sfcValidationStake = self.__sfcContract.getValidationStake(validatorId=validatorId)

        # Calculate staking metrics
        selfStakedAmount = sfcValidationStake[5] / 1e18
        delegatedAmount = sfcValidationStake[7] / 1e18
        inUndelegationAmount = self.__database.getInUndelegationAmount(validatorId=validatorId)
        totalStakedAmount = selfStakedAmount + delegatedAmount

        # Check if validator has been deactivated
        if selfStakedAmount == 0:
            return self

        # Calculate the available delegation capacity
        availableCapacityAmount = selfStakedAmount * 15 - delegatedAmount

        # Check status
        isUnstaking = sfcValidationStake[4] != 0
        isCheater = sfcValidationStake[0] == 1

        self.__data += [{
            "_id": validatorId,
            "name": name,
            "logoUrl": logoUrl,
            "website": website,
            "contact": contact,
            "address": sfcValidationStake[8].lower(),
            "selfStakedAmount": selfStakedAmount,
            "delegatedAmount": delegatedAmount,
            "inUndelegationAmount": inUndelegationAmount,
            "totalStakedAmount": totalStakedAmount,
            "availableCapacityAmount": availableCapacityAmount,
            "stakingPowerPercent": 0,
            "isVerified": isVerified,
            "isCheater": isCheater,
            "isUnstaking": isUnstaking
        }]

        return self

    def setStakingPower(self, totalStakedSum):
        for validator in self.__data:
            validator["stakingPowerPercent"] = validator["totalStakedAmount"] / totalStakedSum

    def save(self):
        if len(self.__data) != 0:
            self.__database.insertOrUpdateValidators(validators=self.__data)

    def getAll(self):
        return self.__data
