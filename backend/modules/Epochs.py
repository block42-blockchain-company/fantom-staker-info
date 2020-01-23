class Epochs:
    def __init__(self, sfc, db):
        self.__sfc = sfc
        self.__db = db

    def __getLatestSyncedEpochId(self):
        epochs = self.__db.table("epochs")
        documents = epochs.all()

        if len(documents) != 0:
            latestSyncedEpochId = max(documents, key=lambda document: document["id"])["id"]
        else:
            latestSyncedEpochId = 0

        return latestSyncedEpochId

    def getAll(self):
        return db.table("epochs").all()

    def update(self):
        latestSyncedEpochId = self.__getLatestSyncedEpochId()
        latestSealedEpochId = self.__sfc.getCurrentSealedEpochId()

        epochs = []

        # Get all new epochs
        for epochId in range(latestSyncedEpochId + 1, latestSealedEpochId + 1):
            epoch = self.__sfc.getEpochSnapshot(epochId)
            epochs += [{
                "id": epochId,
                "epoch": epoch
            }]

        # Update epochs
        self.__db.table("epochs").insert_multiple(epochs)
