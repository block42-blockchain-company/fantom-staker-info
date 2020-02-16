import requests


class BinanceApi:
    def __init__(self):
        self.__url = "https://explorer.binance.org/api/v1/"

    def getTransfers(self, startTime, endTime):
        # Send a request to get the number of tx in this period
        numberOfTx = requests.get(self.__url + "txs?page=1&rows=1&txAsset=FTM-A64&txType=TRANSFER" +
                                  "&startTime=" + str(startTime) +
                                  "&endTime=" + str(endTime)
                                  ).json()["txNums"]

        if numberOfTx > 10000:
            raise ValueError("There are more than 10k transfers")

        # Calculate last page
        lastPage = int(numberOfTx / 100) + 1

        data = []

        for page in range(1, lastPage + 1):
            transfers = requests.get(self.__url + "txs?page=" + str(page) + "&rows=100&txAsset=FTM-A64&txType=TRANSFER" +
                                     "&startTime=" + str(startTime) +
                                     "&endTime=" + str(endTime)
                                     ).json()["txArray"]

            for transfer in transfers:
                # Check whether this is a normal of a batch transfer
                if "fromAddr" in transfer:
                    data += [transfer]
                else:
                    # Get all sub transfers of the batch transfer
                    data += self.__getSubTransfers(txHash=transfer["txHash"], timestamp=transfer["timeStamp"])

        return data

    def __getSubTransfers(self, txHash, timestamp):
        # Send a request to get the number of sub tx
        numberOfSubTx = requests.get(self.__url + "sub-tx-list?page=1&rows=1&txHash=" + txHash).json()["totalNum"]

        if numberOfSubTx > 10000:
            raise ValueError("There are more than 10k sub transfers")

        # Calculate last page
        lastPage = int(numberOfSubTx / 100) + 1

        data = []

        for page in range(1, lastPage + 1):
            subTransfers = requests.get(self.__url + "sub-tx-list?page=" + str(page) + "&rows=100&txHash=" + txHash).json()["subTxDtoList"]

            # Apply tx hash and timestamp from parent batch transfer
            for subTransfer in subTransfers:
                subTransfer["txHash"] = txHash
                subTransfer["timeStamp"] = timestamp

            data += subTransfers

        return data
