from queue import Queue
from threading import Thread


class ERC20Transfers:
    def __init__(self, ethereumApi, database):
        self.__ethereumApi = ethereumApi
        self.__database = database
        self.__data = []

    def __doWork(self, queue):
        while True:
            (fromBlock, toBlock) = queue.get()

            transfers = self.__ethereumApi.getTransfers(fromBlock=fromBlock, toBlock=toBlock)

            print("Syncing ERC20 Transfers from block #" + str(fromBlock) + " to block #" + str(toBlock) + " ...")

            for transfer in transfers:
                self.__data += [{
                    "from": ("0x" + transfer["topics"][1][26:]).lower(),
                    "to": ("0x" + transfer["topics"][2][26:]).lower(),
                    "amount": int(transfer["data"], 16) / 1e18,
                    "block": int(transfer["blockNumber"], 16),
                    "txHash": transfer["transactionHash"]
                }]

            queue.task_done()

    def sync(self):
        lastSyncedERC20TransferBlockHeight = self.__database.getLastSyncedERC20TransferBlockHeight(defaultValue=5792340)
        latestBlockHeight = self.__ethereumApi.getLatestBlockHeight()

        queue = Queue()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(queue,))
            worker.setDaemon(True)
            worker.start()

        fromBlock = lastSyncedERC20TransferBlockHeight

        while fromBlock < latestBlockHeight:
            toBlock = fromBlock + 20000 if fromBlock + 20000 < latestBlockHeight else latestBlockHeight
            queue.put((fromBlock, toBlock))
            fromBlock = toBlock + 1

        queue.join()

        # Save batch to database
        if len(self.__data) != 0:
            self.__database.insertERC20Transfers(transfers=self.__data)

        return self