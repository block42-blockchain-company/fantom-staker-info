import json
import urllib.request

from tinydb import where
from tinydb.operations import set

from modules.DefaultConfig import DefaultConfig


class Validators:
    def __init__(self, sfc, stakerInfo, db):
        self.__sfc = sfc
        self.__stakerInfo = stakerInfo
        self.__db = db
        self.__data = []
        self.__totalSupply = self.__sfc.getTotalSupply()

    def getAll(self):
        return self.__data

    def sync(self, validatorId, deactivatedDelegations):
        # Get the config url from smart contract
        configUrl = self.__stakerInfo.getConfigUrl(validatorId)

        name = ""
        logoUrl = ""
        website = ""
        contact = ""
        isVerified = False

        if configUrl is not "":
            try:
                config = json.loads(urllib.request.urlopen(configUrl).read().decode())

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
            except json.decoder.JSONDecodeError:
                pass
        elif DefaultConfig.containsInfoForValidator(validatorId):
            # No config in smart contract found, use bootstrap values
            name = DefaultConfig.getInfoForValidator(validatorId)["name"]
            website = DefaultConfig.getInfoForValidator(validatorId)["website"]

        # Get validator info from the sfc smart contract
        validatorInfo = self.__sfc.getValidatorInfo(validatorId)

        # Calculate staking metrics
        selfStakedAmount = validatorInfo[5] / 1e18
        delegatedAmount = validatorInfo[7] / 1e18
        inUndelegationAmount = sum(map(lambda delegation: delegation["data"][4] / 1e18, deactivatedDelegations))
        totalStakedAmount = selfStakedAmount + delegatedAmount + inUndelegationAmount

        # Calculate the available delegation capacity
        availableCapacityAmount = selfStakedAmount * 15 - delegatedAmount

        # Check status
        isUnstaking = validatorInfo[4] != 0
        isCheater = (validatorInfo[0] and 1) != 0

        self.__data += [{
            "id": validatorId,
            "name": name,
            "logoUrl": logoUrl,
            "website": website,
            "contact": contact,
            "address": validatorInfo[8],
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
        for validator in self.getAll():
            validator["stakingPowerPercent"] = validator["totalStakedAmount"] / totalStakedSum

    def save(self):
        self.__db.purge_table("validators")
        self.__db.table("validators").insert_multiple(self.__data)
