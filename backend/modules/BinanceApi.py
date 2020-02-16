import requests


class BinanceApi:
    def __init__(self):
        self.__url = "https://explorer.binance.org/api/v1/"

    def getTransfers(self, startTime, endTime):
        numberOfTx = requests.get(self.__url + "txs?page=1&rows=1&txAsset=FTM-A64&txType=TRANSFER" +
                                  "&startTime=" + str(startTime) +
                                  "&endTime=" + str(endTime)
                                  ).json()["txNums"]

        if numberOfTx > 10000:
            raise ValueError("There are more than 10k transfers")

        lastPage = int(numberOfTx / 100) + 1

        data = []

        for page in range(1, lastPage + 1):
            transfers = requests.get(self.__url + "txs?page=" + str(page) + "&rows=100&txAsset=FTM-A64&txType=TRANSFER" +
                                     "&startTime=" + str(startTime) +
                                     "&endTime=" + str(endTime)
                                     ).json()["txArray"]

            for transfer in transfers:
                if "fromAddr" in transfer:
                    data += [transfer]
                else:
                    data += self.__getSubTransfers(txHash=transfer["txHash"], timestamp=transfer["timeStamp"])

        return data

    def __getSubTransfers(self, txHash, timestamp):
        numberOfSubTx = requests.get(self.__url + "sub-tx-list?page=1&rows=1&txHash=" + txHash).json()["totalNum"]

        if numberOfSubTx > 10000:
            raise ValueError("There are more than 10k sub transfers")

        lastPage = int(numberOfSubTx / 100) + 1

        data = []

        for page in range(1, lastPage + 1):
            subTransfers = requests.get(self.__url + "sub-tx-list?page=" + str(page) + "&rows=100&txHash=" + txHash).json()["subTxDtoList"]

            for subTransfer in subTransfers:
                subTransfer["txHash"] = txHash
                subTransfer["timeStamp"] = timestamp

            data += subTransfers

        return data
