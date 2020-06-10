class Delegations:
    def __init__(self, sfcContract, database):
        self.__sfcContract = sfcContract
        self.__database = database
        self.__blocks = self.__database.getAllBlocks()
        self.__data = []

    def __getBlockByHeight(self, blockHeight):
        blocks = list(filter(lambda block: block["_id"] == blockHeight, self.__blocks))
        return blocks[0] if len(blocks) > 0 else None

    def sync(self):
        # Get last synced block number of all delegations
        lastSyncedDelegationBlockHeight = self.__database.getLastSyncedDelegationBlockHeight(defaultValue=-1)

        # Get smart contract events
        createdDelegationEvents = self.__sfcContract.getEvents(eventName="CreatedDelegation", fromBlock=lastSyncedDelegationBlockHeight + 1)
        increasedDelegationEvents = self.__sfcContract.getEvents(eventName="IncreasedDelegation", fromBlock=lastSyncedDelegationBlockHeight + 1)
        preparedToWithdrawDelegationEvents = self.__sfcContract.getEvents(eventName="PreparedToWithdrawDelegation", fromBlock=lastSyncedDelegationBlockHeight + 1)
        deactivatedDelegationEvents = self.__sfcContract.getEvents(eventName="DeactivatedDelegation", fromBlock=lastSyncedDelegationBlockHeight + 1)
        withdrawnDelegationEvents = self.__sfcContract.getEvents(eventName="WithdrawnDelegation", fromBlock=lastSyncedDelegationBlockHeight + 1)

        events = []
        events += list(map(lambda event: {
            "address": event["args"]["delegator"].lower(),
            "validatorId": event["args"]["toStakerID"],
            "amount": event["args"]["amount"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, createdDelegationEvents))
        events += list(map(lambda event: {
            "address": event["args"]["delegator"].lower(),
            "validatorId": event["args"]["stakerID"],
            "newAmount": event["args"]["newAmount"],
            "diff": event["args"]["diff"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, increasedDelegationEvents))
        events += list(map(lambda event: {
            "address": event["args"]["delegator"].lower(),
            "validatorId": event["args"]["stakerID"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, preparedToWithdrawDelegationEvents))
        events += list(map(lambda event: {
            "address": event["args"]["delegator"].lower(),
            "validatorId": event["args"]["stakerID"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, deactivatedDelegationEvents))
        events += list(map(lambda event: {
            "address": event["args"]["delegator"].lower(),
            "validatorId": event["args"]["stakerID"],
            "penalty": event["args"]["penalty"],
            "block": event["blockNumber"],
            "type": event["event"]
        }, withdrawnDelegationEvents))

        # Sort relevant events ascending by block number
        events = filter(lambda event: event["block"] > lastSyncedDelegationBlockHeight, events)
        events = sorted(events, key=lambda event: event["block"], reverse=False)

        # Get all delegations as they might get updated (prepare to withdraw or withdraw)
        self.__data = self.__database.getAllDelegations(sort=-1)

        for event in events:
            block = self.__getBlockByHeight(blockHeight=event["block"])

            # Might be None if epoch has not been sealed yet
            if block is None:
                continue

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
                print("New delegation: " + str(event["amount"] / 1e18) + " FTM (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")
            elif event["type"] == "IncreasedDelegation":
                delegation = sorted(
                    filter(lambda delegation: delegation["address"] == event["address"], self.__data),
                    key=lambda delegation: delegation["block"], reverse=True
                )[0]
                delegation["amount"] = event["newAmount"] / 1e18
                print("Increased delegation: " + str(delegation["amount"]) + " FTM; Diff: " + str(event["diff"] / 1e18) + " FTM; Start epoch: #" + str(delegation["startEpoch"]) + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")
            elif event["type"] == "DeactivatedDelegation" or event["type"] == "PreparedToWithdrawDelegation":
                delegation = sorted(
                    filter(lambda delegation: delegation["address"] == event["address"], self.__data),
                    key=lambda delegation: delegation["block"], reverse=True
                )[0]
                delegation["endEpoch"] = block["epoch"]
                print("Deactivated delegation: " + str(delegation["amount"]) + " FTM; Start epoch: #" + str(delegation["startEpoch"]) + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")
            elif event["type"] == "WithdrawnDelegation":
                delegation = sorted(
                    filter(lambda delegation: delegation["address"] == event["address"], self.__data),
                    key=lambda delegation: delegation["block"], reverse=True
                )[0]
                delegation["withdrawn"] = True
                print("Withdraw delegation: " + str(delegation["amount"]) + " FTM; Start epoch: #" + str(delegation["startEpoch"]) + "; End epoch: #" + str(delegation["endEpoch"]) + " (block #" + str(block["_id"]) + " | epoch #" + str(block["epoch"]) + ") ...")

        # Save to database
        if len(self.__data) != 0:
            self.__database.insertOrUpdateDelegations(delegations=self.__data)

        return self
