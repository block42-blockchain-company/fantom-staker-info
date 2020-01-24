class Epochs:
    def __init__(self, sfc, db):
        self.__sfc = sfc
        self.__db = db
        self.__data = []

    def __getLatestSyncedEpochId(self):
        epochs = self.__db.table("epochs")
        documents = epochs.all()

        if len(documents) != 0:
            latestSyncedEpochId = max(documents, key=lambda document: document["id"])["id"]
        else:
            latestSyncedEpochId = 0

        return latestSyncedEpochId

    def getAll(self):
        return self.__data

    def sync(self):
        latestSyncedEpochId = self.__getLatestSyncedEpochId()
        latestSealedEpochId = self.__sfc.getCurrentSealedEpochId()

        # Get all new epochs
        for epochId in range(latestSyncedEpochId + 1, latestSealedEpochId + 1):
            epoch = self.__sfc.getEpochSnapshot(epochId)

            self.__data += [{
                "id": epochId,
                "epoch": epoch
            }]

        return self

    def save(self):
        self.__db.table("epochs").insert_multiple(self.__data)
