from queue import Queue
from threading import Thread


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

    def __doWork(self, queue):
        while True:
            blockHeight = queue.get()
            block = self.__fantomApi.getBlock(blockHeight)
            epoch = self.__getEpochForTimestamp(timestamp=block["timestamp"])

            # Check if block is in current epoch
            if epoch is None:
                epochId = self.__currentEpoch
            else:
                epochId = epoch["_id"]

            print("Syncing block #" + str(blockHeight) + " (epoch #" + str(epochId) + ") ...")

            self.__data += [{
                "_id": block["number"],
                "epoch": epochId,
                "timestamp": block["timestamp"],
                "transactions": list(map(lambda transaction: transaction.hex(), block["transactions"]))
            }]

            queue.task_done()

    def sync(self):
        lastSyncedBlockHeight = self.__database.getLastSyncedBlockHeight(defaultValue=-1)
        latestBlockHeight = self.__fantomApi.getLatestBlockNumber()

        queue = Queue()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(queue,))
            worker.setDaemon(True)
            worker.start()

        batchCount = 0

        # Add all block heights that need to be synced to the queue
        for blockHeight in range(lastSyncedBlockHeight + 1, latestBlockHeight + 1):
            # Add work to queue
            queue.put(blockHeight)

            batchCount += 1

            # Batch work into size of 1k
            if batchCount == 1000 or blockHeight == latestBlockHeight:
                # Wait for batch to finish
                queue.join()

                # Save batch to database
                if len(self.__data) != 0:
                    self.__database.insertBlocks(blocks=self.__data)

                # Reset batch
                batchCount = 0
                self.__data = []

        return self
