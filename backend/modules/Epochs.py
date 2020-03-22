import concurrent.futures


class Epochs:
    def __init__(self, sfcContract, database):
        self.__sfcContract = sfcContract
        self.__database = database
        self.__data = []

    def __getEpochValidator(self, epochId, validatorId):
        data = self.__sfcContract.getEpochValidator(epochId, validatorId)

        # Only add validators that were present in the epoch
        if sum(data) == 0:
            return None

        return {
            "id": validatorId,
            "stakeAmount": data[0] / 1e18,
            "delegatedMe": data[1] / 1e18,
            "baseRewardWeight": data[2] / 1e18,
            "txRewardWeight": data[3] / 1e18
        }

    def __getEpoch(self, epochId, validatorCount):
        epoch = self.__sfcContract.getEpochSnapshot(epochId)

        print("Syncing epoch #" + str(epochId) + " ...")

        validators = []

        # Get data for every validator in the epoch
        for validatorId in range(1, validatorCount + 1):
            validator = self.__getEpochValidator(epochId, validatorId)
            validators += [validator] if validator is not None else []

        return {
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
        }

    def sync(self):
        lastSyncedEpochId = self.__database.getLastSyncedEpochId(defaultValue=0)
        latestSealedEpochId = self.__sfcContract.getCurrentSealedEpochId()
        validatorCount = self.__sfcContract.getValidatorCount()

        epochIds = range(lastSyncedEpochId + 1, latestSealedEpochId + 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futureToEpoch = {pool.submit(self.__getEpoch, epochId, validatorCount) for epochId in epochIds}

            for future in concurrent.futures.as_completed(futureToEpoch):
                epoch = future.result()
                self.__data += [epoch]

            if len(self.__data) != 0:
                self.__database.insertEpochs(epochs=self.__data)

        return self
