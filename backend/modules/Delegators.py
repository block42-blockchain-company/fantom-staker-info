import json
import urllib.request

from tinydb import where


class Delegators:
    def __init__(self, db):
        self.__db = db
        self.__data = []

    def getAll(self):
        return self.__data

    def sync(self, validatorId):
        # Get delegation addresses
        response = json.loads(urllib.request.urlopen("https://api.fantom.network/api/v1/delegator/staker/" + str(validatorId) + "?verbosity=0").read().decode())
        delegatorAddresses = response["data"]["delegators"]

        self.__data += [{
            "validatorId": validatorId,
            "delegators": delegatorAddresses
        }]

        return self

    def save(self):
        self.__db.purge_table("delegators")
        self.__db.table("delegators").insert_multiple(self.__data)