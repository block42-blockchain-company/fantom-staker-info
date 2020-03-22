import concurrent.futures


class Transactions:
    def __init__(self, fantomApi, database):
        self.__fantomApi = fantomApi
        self.__database = database
        self.__data = []

    def __getTransactions(self, block):
        transactions = []

        for txHash in block["transactions"]:
            print("Syncing transaction " + txHash + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")

            transaction = self.__fantomApi.getTransaction(txHash=txHash)
            transactionReceipt = self.__fantomApi.getTransactionReceipt(txHash=txHash)

            transactions += [{
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

        return transactions

    def sync(self):
        lastSyncedTransactionBlockHeight = self.__database.getLastSyncedTransactionBlockHeight(defaultValue=-1)
        blocks = self.__database.getAllBlocks(sort=1, skip=lastSyncedTransactionBlockHeight + 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futureToEpoch = {pool.submit(self.__getTransactions, block) for block in blocks}

            for future in concurrent.futures.as_completed(futureToEpoch):
                block = future.result()
                self.__data += block

        if len(self.__data) != 0:
            self.__database.insertTransactions(transactions=self.__data)

        return self
