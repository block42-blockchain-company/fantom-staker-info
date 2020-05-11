import concurrent.futures


class Events:
    def __init__(self, fantomApi, database):
        self.__fantomApi = fantomApi
        self.__database = database
        self.__data = []

    def __getEvents(self, epochId):
        print("Syncing events (epoch #" + str(epochId) + ") ...")

        eventIds = self.__fantomApi.getAllEpochEvents(epochId=epochId)

        events = []

        for eventId in eventIds:
            event = self.__fantomApi.getEpochEvent(eventId=eventId)

            # Events might not be found for some reason
            if event is not None:
                event["_id"] = event.pop("hash")
                events += [event]

        return events

    def sync(self):
        lastSyncedEventEpochId = self.__database.getLastSyncedEventEpochId(defaultValue=0)
        lastSyncedEpochId = self.__database.getLastSyncedEpochId(defaultValue=0)

        eventEpochIdsToSync = range(lastSyncedEventEpochId + 1, lastSyncedEpochId + 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futureToEpoch = {pool.submit(self.__getEvents, epochId) for epochId in eventEpochIdsToSync}

            for future in concurrent.futures.as_completed(futureToEpoch):
                events = future.result()
                self.__data += events

        if len(self.__data) != 0:
            self.__database.insertEvents(events=self.__data)

        return self
