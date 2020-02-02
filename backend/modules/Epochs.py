from queue import Queue
from threading import Thread


class Epochs:
    def __init__(self, sfcContract, database):
        self.__sfcContract = sfcContract
        self.__database = database
        self.__data = []

    def __doWork(self, epochQueue, validatorCount):
        while True:
            epochId = epochQueue.get()
            epoch = self.__sfcContract.getEpochSnapshot(epochId)

            print("Syncing epoch #" + str(epochId) + " ...")

            validators = []

            # Get data for every validator in the epoch
            for validatorId in range(1, validatorCount + 1):
                data = self.__sfcContract.getEpochValidator(epochId, validatorId)

                # Only add validators that were present in the epoch
                if sum(data) == 0:
                    continue

                validators += [{
                    "id": validatorId,
                    "stakeAmount": data[0] / 1e18,
                    "delegatedMe": data[1] / 1e18,
                    "baseRewardWeight": data[2] / 1e18,
                    "txRewardWeight": data[3] / 1e18
                }]

            self.__data += [{
                "_id": epochId,
                "endTime": epoch[0],
                "duration": epoch[1],
                "epochFee": epoch[2] / 1e18,
                "totalBaseRewardWeight": epoch[3] / 1e18,
                "totalTxRewardWeight": epoch[4] / 1e18,
                "baseRewardPerSecond": epoch[5] / 1e18,
                "stakeTotalAmount": epoch[6] / 1e18,
                "delegationsTotalAmount": epoch[7] / 1e18,
                "totalSupply": epoch[8] / 1e18,
                "validators": validators
            }]

            epochQueue.task_done()

    def sync(self):
        lastSyncedEpochId = self.__database.getLastSyncedEpochId(defaultValue=0)
        latestSealedEpochId = self.__sfcContract.getCurrentSealedEpochId()

        epochQueue = Queue()

        # Add all epoch ids that need to be synced to the queue
        for epochId in range(lastSyncedEpochId + 1, latestSealedEpochId + 1):
            epochQueue.put(epochId)

        # Get the validator count so the workers do not need to query it
        validatorCount = self.__sfcContract.getValidatorCount()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(epochQueue, validatorCount,))
            worker.setDaemon(True)
            worker.start()

        # Wait for workers to finish
        epochQueue.join()

        # Sort ascending (workers added it in whatever order)
        self.__data = sorted(self.__data, key=lambda epoch: epoch["_id"], reverse=False)

        return self

    def save(self):
        if len(self.__data) != 0:
            self.__database.insertEpochs(epochs=self.__data)
