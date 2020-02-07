from queue import Queue
from threading import Thread


class Events:
    def __init__(self, fantomApi, database):
        self.__fantomApi = fantomApi
        self.__database = database
        self.__data = []

    def __doWork(self, epochQueue):
        while True:
            epochId = epochQueue.get()

            print("Syncing events (epoch #" + str(epochId) + ") ...")

            eventIds = self.__fantomApi.getAllEpochEvents(epochId=epochId)

            for eventId in eventIds:
                event = self.__fantomApi.getEpochEvent(eventId=eventId)
                event["_id"] = event.pop("hash")
                self.__data += [event]

            epochQueue.task_done()

    def sync(self):
        lastSyncedEventEpochId = self.__database.getLastSyncedEventEpochId(defaultValue=0)
        lastSyncedEpochId = self.__database.getLastSyncedEpochId(defaultValue=0)

        epochQueue = Queue()

        # Add all epoch ids that need to be synced to the queue
        for epochId in range(lastSyncedEventEpochId + 1, lastSyncedEpochId + 1):
            epochQueue.put(epochId)

        for i in range(10):
            worker = Thread(target=self.__doWork, args=(epochQueue,))
            worker.setDaemon(True)
            worker.start()

        # Wait for workers to finish
        epochQueue.join()

        # Sort ascending (workers added it in whatever order)
        self.__data = sorted(self.__data, key=lambda event: event["epoch"], reverse=False)

        return self

    def save(self):
        if len(self.__data) != 0:
            self.__database.insertEvents(events=self.__data)
