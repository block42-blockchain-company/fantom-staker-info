import moment
import concurrent.futures


class BEP2Transfers:
    def __init__(self, binanceApi, database):
        self.__binanceApi = binanceApi
        self.__database = database
        self.__data = []

    def __getTransfers(self, timeRange):
        startTime = timeRange["startTime"]
        endTime = timeRange["endTime"]

        print("Syncing BEP2 transfers until " + moment.unix(endTime).format("DD.MM.YYYY @ HH:mm") + " ...")

        transfers = self.__binanceApi.getTransfers(startTime=startTime, endTime=endTime)

        data = []

        for transfer in transfers:
            data += [{
                "from": transfer["fromAddr"],
                "to": transfer["toAddr"],
                "amount": transfer["value"],
                "timestamp": transfer["timeStamp"],
                "txHash": transfer["txHash"]
            }]

        return data

    def sync(self):
        # BEP2 transfer timestamps are in milli seconds (1556668800000 was the first time of a BEP2 transfer)
        lastSyncedERC20TransferTimestamp = self.__database.getLastSyncedBEP2TransferTimestamp(defaultValue=1556668800000)
        now = int(moment.now().datetime.timestamp()) * 1000

        oneWeekInMsSeconds = 7 * 24 * 60 * 60 * 1000
        startTime = lastSyncedERC20TransferTimestamp + 1 * 1000

        timeRanges = []

        while startTime < now:
            endTime = startTime + oneWeekInMsSeconds if startTime + oneWeekInMsSeconds < now else now
            timeRanges += [{"startTime": startTime, "endTime": endTime}]
            startTime = endTime + 1 * 1000

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futureToEpoch = {pool.submit(self.__getTransfers, timeRange) for timeRange in timeRanges}

            for future in concurrent.futures.as_completed(futureToEpoch):
                transfers = future.result()
                self.__data += transfers

        if len(self.__data) != 0:
            self.__database.insertBEP2Transfers(transfers=self.__data)

        return self
