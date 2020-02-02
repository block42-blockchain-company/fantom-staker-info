from queue import Queue
from threading import Thread


class Transactions:
    def __init__(self, web3, database):
        self.__web3 = web3
        self.__database = database
        self.__blocks = self.__database.getAllBlocks()
        self.__data = []

    def __doWork(self, blockQueue):
        while True:
            block = blockQueue.get()

            for transactionId in block["transactions"]:
                print("Syncing transaction " + transactionId + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")

                transaction = self.__web3.getTransaction(transactionId)

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
        lastSyncedTransactionBlockNumber = self.__database.getLastSyncedTransactionBlockNumber(defaultValue=0)
        self.__blocks = self.__blocks[lastSyncedTransactionBlockNumber:]

        blockQueue = Queue()

        # Add all block numbers that need to be synced to the queue
        for block in self.__blocks:
            blockQueue.put(block)

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(blockQueue,))
            worker.setDaemon(True)
            worker.start()

        # Wait for workers to finish
        blockQueue.join()

        # Sort ascending (workers added it in whatever order)
        self.__data = sorted(self.__data, key=lambda transaction: transaction["_id"], reverse=False)

        return self

    def save(self):
        if len(self.__data) != 0:
            self.__database.insertTransactions(transactions=self.__data)
