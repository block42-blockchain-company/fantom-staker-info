class Epochs:
    def __init__(self, sfc, db):
        self.__sfc = sfc
        self.__db = db
        self.__data = []

    def getAll(self):
        return self.__data + self.__db.table("epochs").all() if len(self.__data) != 0 else self.__db.table("epochs").all()

    def sync(self):
        latestSyncedEpochId = 0 if len(self.getAll()) == 0 else max(self.getAll(), key=lambda epoch: epoch["id"])["id"]
        latestSealedEpochId = self.__sfc.getCurrentSealedEpochId()

        # Get all new epochs
        for epochId in range(latestSyncedEpochId + 1, latestSealedEpochId + 1):
            epoch = self.__sfc.getEpochSnapshot(epochId)

            validators = []

            for validatorId in range(1, self.__sfc.getValidatorCount()):
                validators += [{
                    "id": validatorId,
                    "data": self.__sfc.getEpochValidator(epochId, validatorId)
                }]

            self.__data += [{
                "id": epochId,
                "data": epoch,
                "validators": validators
            }]

        return self

    def save(self):
        self.__db.table("epochs").insert_multiple(self.__data)
