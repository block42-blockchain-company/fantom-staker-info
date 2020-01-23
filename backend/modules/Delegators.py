import json
import urllib.request

from tinydb import where


class Delegators:
    __list = []

    def __init__(self, db):
        self.__db = db

    def getAll(self):
        return self.__list

    def add(self, validatorId):
        # Get delegation addresses
        response = json.loads(urllib.request.urlopen("https://api.fantom.network/api/v1/delegator/staker/" + str(validatorId) + "?verbosity=0").read().decode())
        delegatorAddresses = response["data"]["delegators"]

        delegator = {
            "validatorId": validatorId,
            "delegators": delegatorAddresses
        }

        self.__db.table("delegators").upsert(delegator, where("validatorId") == validatorId)
        self.__list += [delegator]
