class Delegations:
    def __init__(self, sfcContract, database):
        self.__sfcContract = sfcContract
        self.__database = database
        self.__blocks = self.__database.getAllBlocks()
        self.__data = []

    def __getBlockByNumber(self, blockNumber):
        blocks = list(filter(lambda block: block["_id"] == blockNumber, self.__blocks))
        return blocks[0] if len(blocks) > 0 else None

    def sync(self):
        # Get smart contract events
        createdDelegationEvents = self.__sfcContract.getEvents(eventName="CreatedDelegation")
        preparedToWithdrawDelegationEvents = self.__sfcContract.getEvents(eventName="PreparedToWithdrawDelegation")
        withdrawnDelegationEvents = self.__sfcContract.getEvents(eventName="WithdrawnDelegation")

        events = []
        events += list(map(lambda event: {
            "address": event["args"]["from"],
            "validatorId": event["args"]["toStakerID"],
            "amount": event["args"]["amount"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, createdDelegationEvents))
        events += list(map(lambda event: {
            "address": event["args"]["from"],
            "validatorId": event["args"]["stakerID"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, preparedToWithdrawDelegationEvents))
        events += list(map(lambda event: {
            "address": event["args"]["from"],
            "validatorId": event["args"]["stakerID"],
            "penalty": event["args"]["penalty"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, withdrawnDelegationEvents))

        # Get last synced block number of all delegations
        lastSyncedDelegationBlockNumber = self.__database.getLastSyncedDelegationBlockNumber(defaultValue=-1)

        # Sort relevant events ascending by block number
        events = filter(lambda event: event["block"] > lastSyncedDelegationBlockNumber, events)
        events = sorted(events, key=lambda event: event["block"], reverse=False)

        # Get all delegations as they might get updated (prepare to withdraw or withdraw)
        self.__data = self.__database.getAllDelegations()

        for event in events:
            block = self.__getBlockByNumber(blockNumber=event["block"])

            # Might be None if epoch has not been sealed yet
            if block is None:
                continue

            print("Syncing delegation (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")

            if event["type"] == "CreatedDelegation":
                self.__data += [{
                    "address": event["address"],
                    "validatorId": event["validatorId"],
                    "amount": event["amount"] / 1e18,
                    "block": block["_id"],
                    "startEpoch": block["epoch"],
                    "endEpoch": 0,
                    "withdrawn": False
                }]
            elif event["type"] == "PreparedToWithdrawDelegation":
                delegation = sorted(
                    filter(lambda delegation: delegation["address"] == event["address"], self.__data),
                    key=lambda delegation: delegation["block"], reverse=True
                )[0]
                delegation["endEpoch"] = block["epoch"]
            elif event["type"] == "WithdrawnDelegation":
                delegation = sorted(
                    filter(lambda delegation: delegation["address"] == event["address"], self.__data),
                    key=lambda delegation: delegation["block"], reverse=True
                )[0]
                delegation["withdrawn"] = True

        # Save to database
        if len(self.__data) != 0:
            self.__database.insertOrUpdateDelegations(delegations=self.__data)

        return self
