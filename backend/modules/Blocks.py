from queue import Queue
from threading import Thread


class Blocks:
    def __init__(self, web3, database):
        self.__web3 = web3
        self.__database = database
        self.__epochs = self.__database.getAllEpochs()
        self.__data = []

    def __getEpochForTimestamp(self, timestamp):
        epochs = list(filter(lambda epoch: epoch["data"]["endTime"] >= timestamp >= epoch["data"]["endTime"] - epoch["data"]["duration"], self.__epochs))
        return epochs[0] if len(epochs) > 0 else None

    def __doWork(self, blockQueue):
        while True:
            blockNumber = blockQueue.get()
            block = self.__web3.getBlock(blockNumber)
            epoch = self.__getEpochForTimestamp(timestamp=block["timestamp"])

            if epoch is None:
                blockQueue.task_done()
                continue

            print("Syncing block #" + str(blockNumber) + " (epoch #" + str(epoch["_id"]) + ") ...")

            self.__data += [{
                "_id": blockNumber,
                "epoch": epoch["_id"]
            }]

            blockQueue.task_done()

    def sync(self):
        lastSyncedBlockNumber = self.__database.getLastSyncedBlockNumber(defaultValue=-1)
        latestBlockNumber = self.__web3.getLatestBlockNumber()

        blockQueue = Queue()

        # Add all block numbers that need to be synced to the queue
        for blockNumber in range(lastSyncedBlockNumber + 1, latestBlockNumber + 1):
            blockQueue.put(blockNumber)

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(blockQueue,))
            worker.setDaemon(True)
            worker.start()

        # Wait for workers to finish
        blockQueue.join()

        # Sort ascending (workers added it in whatever order)
        self.__data = sorted(self.__data, key=lambda block: block["_id"], reverse=False)

        return self

    def save(self):
        if len(self.__data) != 0:
            self.__database.insertBlocks(blocks=self.__data)
