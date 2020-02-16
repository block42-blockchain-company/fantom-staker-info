import moment

from queue import Queue
from threading import Thread


class BEP2Transfers:
    def __init__(self, binanceApi, database):
        self.__binanceApi = binanceApi
        self.__database = database
        self.__data = []

    def __doWork(self, queue):
        while True:
            (startTime, endTime) = queue.get()

            print("Syncing BEP2 Transfers until " + moment.unix(endTime).format("DD.MM.YYYY") + " ...")

            transfers = self.__binanceApi.getTransfers(startTime=startTime, endTime=endTime)

            for transfer in transfers:
                self.__data += [{
                    "from": transfer["fromAddr"],
                    "to": transfer["toAddr"],
                    "amount": transfer["value"],
                    "timestamp": transfer["timeStamp"],
                    "txHash": transfer["txHash"]
                }]

            queue.task_done()

    def sync(self):
        # BEP2 transfer timestamps are in milli seconds (1556668800000 was the first time of a BEP2 transfer)
        lastSyncedERC20TransferTimestamp = self.__database.getLastSyncedBEP2TransferTimestamp(defaultValue=1556668800000)
        now = int(moment.now().datetime.timestamp()) * 1000

        queue = Queue()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(queue,))
            worker.setDaemon(True)
            worker.start()

        oneWeekInMsSeconds = 7 * 24 * 60 * 60 * 1000
        startTime = lastSyncedERC20TransferTimestamp + 1 * 1000

        # Calculate time periods to sync
        while startTime < now:
            endTime = startTime + oneWeekInMsSeconds if startTime + oneWeekInMsSeconds < now else now
            queue.put((startTime, endTime))
            startTime = endTime + 1 * 1000

        # Wait to finish
        queue.join()

        # Save to database
        if len(self.__data) != 0:
            self.__database.insertBEP2Transfers(transfers=self.__data)

        return self
