import concurrent.futures


class Blocks:
    def __init__(self, sfcContract, fantomApi, database):
        self.__sfcContract = sfcContract
        self.__fantomApi = fantomApi
        self.__database = database
        self.__epochs = self.__database.getAllEpochs()
        self.__currentEpoch = self.__sfcContract.instance().functions.currentEpoch().call()
        self.__data = []

    def __getEpochForTimestamp(self, timestamp):
        epochs = list(filter(lambda epoch: epoch["endTime"] >= timestamp >= epoch["endTime"] - epoch["duration"], self.__epochs))
        return epochs[0] if len(epochs) > 0 else None

    def __getBlock(self, blockHeight):
        block = self.__fantomApi.getBlock(blockHeight)
        epoch = self.__getEpochForTimestamp(timestamp=block["timestamp"])

        # Check if block is in current epoch
        if epoch is None:
            epochId = self.__currentEpoch
        else:
            epochId = epoch["_id"]

        print("Syncing block #" + str(blockHeight) + " (epoch #" + str(epochId) + ") ...")

        return {
            "_id": block["number"],
            "epoch": epochId,
            "timestamp": block["timestamp"],
            "transactions": list(map(lambda transaction: transaction.hex(), block["transactions"]))
        }

    def sync(self):
        lastSyncedBlockHeight = self.__database.getLastSyncedBlockHeight(defaultValue=-1)
        latestBlockHeight = self.__fantomApi.getLatestBlockNumber()

        blockHeights = range(lastSyncedBlockHeight + 1, latestBlockHeight + 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futureToEpoch = {pool.submit(self.__getBlock, blockHeight) for blockHeight in blockHeights}

            for future in concurrent.futures.as_completed(futureToEpoch):
                block = future.result()
                self.__data += [block]

        if len(self.__data) != 0:
            self.__database.insertBlocks(blocks=self.__data)

        return self
