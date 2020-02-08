from queue import Queue
from threading import Thread


class Transactions:
    def __init__(self, fantomApi, database):
        self.__fantomApi = fantomApi
        self.__database = database
        self.__data = []

    def __doWork(self, blockQueue):
        while True:
            block = blockQueue.get()

            for transactionId in block["transactions"]:
                print("Syncing transaction " + transactionId + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")

                transaction = self.__fantomApi.getTransaction(transactionId)

                self.__data += [{
                    "_id": transaction["hash"].hex(),
                    "from": transaction["from"],
                    "to": transaction["to"],
                    "value": transaction["value"] / 1e18,
                    "input": transaction["input"],
                    "block": transaction["blockNumber"],
                    "epoch": block["epoch"]
                }]

            blockQueue.task_done()

    def sync(self):
        lastSyncedTransactionBlockNumber = self.__database.getLastSyncedTransactionBlockNumber(defaultValue=-1)
        lastSyncedBlockNumber = self.__database.getLastSyncedBlockNumber(defaultValue=0)

        blocks = self.__database.getAllBlocks()[(lastSyncedTransactionBlockNumber + 1):]

        blockQueue = Queue()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(blockQueue,))
            worker.setDaemon(True)
            worker.start()

        batchCount = 0

        # Add all block numbers that need to be synced to the queue
        for block in blocks:
            # Add work to queue
            blockQueue.put(block)

            batchCount += 1

            # Batch work into size of 1k
            if batchCount == 1000 or block["_id"] == lastSyncedBlockNumber:
                # Wait for batch to finish
                blockQueue.join()

                # Save batch to database
                if len(self.__data) != 0:
                    self.__database.insertTransactions(transactions=self.__data)

                # Reset batch
                batchCount = 0
                self.__data = []

        return self
