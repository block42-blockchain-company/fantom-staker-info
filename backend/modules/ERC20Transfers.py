import concurrent.futures


class ERC20Transfers:
    def __init__(self, ethereumApi, database):
        self.__ethereumApi = ethereumApi
        self.__database = database
        self.__data = []

    def __getTransfers(self, blockRange):
        fromBlock = blockRange["fromBlock"]
        toBlock = blockRange["toBlock"]

        print("Syncing ERC20 Transfers until block #" + str(toBlock) + " ...")

        transfers = self.__ethereumApi.getTransfers(fromBlock=fromBlock, toBlock=toBlock)

        data = []

        for transfer in transfers:
            data += [{
                "from": ("0x" + transfer["topics"][1][26:]).lower(),
                "to": ("0x" + transfer["topics"][2][26:]).lower(),
                "amount": int(transfer["data"], 16) / 1e18,
                "block": int(transfer["blockNumber"], 16),
                "txHash": transfer["transactionHash"]
            }]

        return data

    def sync(self):
        # Block 5792340 was the first block with a transfer in it
        lastSyncedERC20TransferBlockHeight = self.__database.getLastSyncedERC20TransferBlockHeight(defaultValue=5792340)
        latestBlockHeight = self.__ethereumApi.getLatestBlockHeight()

        fromBlock = lastSyncedERC20TransferBlockHeight

        blockRanges = []

        while fromBlock < latestBlockHeight:
            toBlock = fromBlock + 20000 if fromBlock + 20000 < latestBlockHeight else latestBlockHeight
            blockRanges += [{"fromBlock": fromBlock, "toBlock": toBlock}]
            fromBlock = toBlock + 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futureToEpoch = {pool.submit(self.__getTransfers, blockRange) for blockRange in blockRanges}

            for future in concurrent.futures.as_completed(futureToEpoch):
                transfers = future.result()
                self.__data += transfers

        if len(self.__data) != 0:
            self.__database.insertERC20Transfers(transfers=self.__data)

        return self
