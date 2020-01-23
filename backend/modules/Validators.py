import json
import urllib.request

from tinydb import where
from .DefaultConfig import DefaultConfig


class Validators:
    __list = []

    def __init__(self, sfc, stakerInfo, db):
        self.__sfc = sfc
        self.__stakerInfo = stakerInfo
        self.__db = db

    def getAll(self):
        return self.__list

    def add(self, validatorId, deactivatedDelegations):
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
            except json.decoder.JSONDecodeError:
                pass
        elif DefaultConfig.containsInfoForValidator(validatorId):
            # No config in smart contract found, use bootstrap values
            name = DefaultConfig.getInfoForValidator(validatorId)["name"]
            website = DefaultConfig.getInfoForValidator(validatorId)["website"]

        # Get validator info from the sfc smart contract
        validatorInfo = self.__sfc.getValidatorInfo(validatorId)
        selfStakedAmount = validatorInfo[5] / 1e18
        delegatedAmount = validatorInfo[7] / 1e18

        # Calculate the available delegation capacity
        availableCapacityAmount = selfStakedAmount * 15 - delegatedAmount

        # Check status
        isUnstaking = validatorInfo[4] != 0
        isCheater = (validatorInfo[0] and 1) != 0

        # Calculate total staked amount
        totalStakedAmount = selfStakedAmount + delegatedAmount

        validator = {
            "id": validatorId,
            "name": name,
            "logoUrl": logoUrl,
            "website": website,
            "contact": contact,
            "address": validatorInfo[8],
            "selfStakedAmount": selfStakedAmount,
            "delegatedAmount": delegatedAmount,
            "totalStakedAmount": totalStakedAmount,
            "availableCapacityAmount": availableCapacityAmount,
            "inUndelegationAmount": sum(map(lambda address: address["delegation"][4], deactivatedDelegations)),
            "isVerified": isVerified,
            "isCheater": isCheater,
            "isUnstaking": isUnstaking
        }

        self.__db.table("validators").upsert(validator, where("id") == validatorId)
        self.__list += [validator]
