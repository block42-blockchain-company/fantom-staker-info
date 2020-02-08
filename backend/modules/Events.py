from queue import Queue
from threading import Thread


class Events:
    def __init__(self, fantomApi, database):
        self.__fantomApi = fantomApi
        self.__database = database
        self.__data = []

    def __doWork(self, queue):
        while True:
            epochId = queue.get()

            print("Syncing events (epoch #" + str(epochId) + ") ...")

            eventIds = self.__fantomApi.getAllEpochEvents(epochId=epochId)

            for eventId in eventIds:
                event = self.__fantomApi.getEpochEvent(eventId=eventId)
                event["_id"] = event.pop("hash")
                self.__data += [event]

            queue.task_done()

    def sync(self):
        lastSyncedEventEpochId = self.__database.getLastSyncedEventEpochId(defaultValue=0)
        lastSyncedEpochId = self.__database.getLastSyncedEpochId(defaultValue=0)

        queue = Queue()

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(queue,))
            worker.setDaemon(True)
            worker.start()

        batchCount = 0

        # Add all epoch ids that need to be synced to the queue
        for epochId in range(lastSyncedEventEpochId + 1, lastSyncedEpochId + 1):
            # Add work to queue
            queue.put(epochId)

            batchCount += 1

            # Batch work into size of 1k
            if batchCount == 1000 or epochId == lastSyncedEpochId:
                # Wait for batch to finish
                queue.join()

                # Save batch to database
                if len(self.__data) != 0:
                    self.__database.insertEvents(events=self.__data)

                # Reset batch
                batchCount = 0
                self.__data = []

        return self
