from queue import Queue
from threading import Thread


class Transactions:
    def __init__(self, fantomApi, database):
        self.__fantomApi = fantomApi
        self.__database = database
        self.__data = []

    def __doWork(self, queue):
        while True:
            block = queue.get()

            for txHash in block["transactions"]:
                print("Syncing transaction " + txHash + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")

                transaction = self.__fantomApi.getTransaction(txHash=txHash)
                transactionReceipt = self.__fantomApi.getTransactionReceipt(txHash=txHash)

                self.__data += [{
                    "_id": transaction["hash"].hex(),
                    "from": str(transaction["from"]).lower(),
                    "to": str(transaction["to"]).lower(),
                    "value": transaction["value"] / 1e18,
                    "gas": transaction["gas"],
                    "gasPrice": transaction["gasPrice"],
                    "input": transaction["input"] if transaction["input"] != "0x" else "",
                    "block": transaction["blockNumber"],
                    "epoch": block["epoch"],
                    "receipt": {
                        "cumulativeGasUsed": transactionReceipt["cumulativeGasUsed"],
                        "gasUsed": transactionReceipt["gasUsed"],
                        "status": transactionReceipt["status"]
                    }
                }]

            queue.task_done()

    def sync(self):
        lastSyncedTransactionBlockHeight = self.__database.getLastSyncedTransactionBlockHeight(defaultValue=-1)
        lastSyncedBlockHeight = self.__database.getLastSyncedBlockHeight(defaultValue=0)

        blocks = self.__database.getAllBlocks(sort=1, skip=lastSyncedTransactionBlockHeight + 1)

        queue = Queue()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(queue,))
            worker.setDaemon(True)
            worker.start()

        batchCount = 0

        # Add all block heights that need to be synced to the queue
        for block in blocks:
            # Add work to queue
            queue.put(block)

            batchCount += 1

            # Batch work into size of 1k
            if batchCount == 1000 or block["_id"] == lastSyncedBlockHeight:
                # Wait for batch to finish
                queue.join()

                # Save batch to database
                if len(self.__data) != 0:
                    self.__database.insertTransactions(transactions=self.__data)

                # Reset batch
                batchCount = 0
                self.__data = []

        return self
