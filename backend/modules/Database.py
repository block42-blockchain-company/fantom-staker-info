import os
import pymongo


class Database:
    def __init__(self):
        self.__instance = pymongo.MongoClient(os.environ["MONGO_URL"]).fantom

    def instance(self):
        return self.__instance

    def dropAll(self):
        self.instance().epochs.drop()
        self.instance().events.drop()
        self.instance().blocks.drop()
        self.instance().transactions.drop()
        self.instance().delegations.drop()
        self.instance().validators.drop()
        self.instance().rewards.drop()
        self.instance().general.drop()

    """
    ### Epochs
    """

    def getLastSyncedEpochId(self, defaultValue):
        lastSyncedEpoch = self.instance().epochs.find_one(sort=[("_id", pymongo.DESCENDING)])
        return defaultValue if lastSyncedEpoch is None else lastSyncedEpoch["_id"]

    def getAllEpochs(self, sort=1, skip=0):
        return list(self.instance().epochs.find(sort=[("_id", sort)], skip=skip))

    def insertEpochs(self, epochs):
        self.instance().epochs.insert_many(epochs)

    """
    ### Events
    """

    def getLastSyncedEventEpochId(self, defaultValue):
        lastSyncedEventEpoch = self.instance().events.find_one(sort=[("epoch", pymongo.DESCENDING)])
        return defaultValue if lastSyncedEventEpoch is None else lastSyncedEventEpoch["epoch"]

    def insertEvents(self, events):
        self.instance().events.insert_many(events)

    """
    ### Blocks
    """

    def getLastSyncedBlockHeight(self, defaultValue):
        lastSyncedBlock = self.instance().blocks.find_one(sort=[("_id", pymongo.DESCENDING)])
        return defaultValue if lastSyncedBlock is None else lastSyncedBlock["_id"]

    def getAllBlocks(self, sort=1, skip=0):
        return list(self.instance().blocks.find(sort=[("_id", sort)], skip=skip))

    def insertBlocks(self, blocks):
        self.instance().blocks.insert_many(blocks)

    """
    ### Transactions
    """

    def getLastSyncedTransactionBlockHeight(self, defaultValue):
        lastSyncedTransactionBlock = self.instance().transactions.find_one(sort=[("block", pymongo.DESCENDING)])
        return defaultValue if lastSyncedTransactionBlock is None else lastSyncedTransactionBlock["block"]

    def getAllTransactions(self):
        return list(self.instance().transactions.find())

    def insertTransactions(self, transactions):
        self.instance().transactions.insert_many(transactions)

    """
    ### Delegations
    """

    def getLastSyncedDelegationBlockHeight(self, defaultValue):
        lastSyncedDelegation = self.instance().delegations.find_one(sort=[("block", pymongo.DESCENDING)])
        return defaultValue if lastSyncedDelegation is None else lastSyncedDelegation["block"]

    def getInUndelegationAmount(self, validatorId):
        query = list(self.instance().delegations.aggregate([
            {"$match": {"endEpoch": {"$ne": 0}, "withdrawn": False, "validatorId": validatorId}},
            {"$group": {"_id": "null", "amount": {"$sum": "$amount"}}}
        ]))
        return 0 if len(query) == 0 else query[0]["amount"]

    def getAllDelegations(self, sort=1, skip=0):
        return list(self.instance().delegations.find(sort=[("_id", sort)], skip=skip))

    def getAllActiveEpochDelegations(self, epochId):
        return list(self.instance().delegations.find({
            "startEpoch": {"$lte": epochId},
            "endEpoch": 0
        }))

    def getAllInactiveEpochDelegations(self, epochId):
        return list(self.instance().delegations.find({
            "startEpoch": {"$lte": epochId},
            "endEpoch": {"$gt": epochId}
        }))

    def insertOrUpdateDelegations(self, delegations):
        self.instance().delegations.drop()
        self.instance().delegations.insert_many(delegations)

    """
    ### Validators
    """

    def insertOrUpdateValidators(self, validators):
        self.instance().validators.drop()
        self.instance().validators.insert_many(validators)

    """
    ### Rewards
    """

    def getAllRewards(self):
        return list(self.instance().rewards.find())

    def getLastSyncedRewardEpochId(self, defaultValue):
        lastSyncedRewardEpochReward = self.instance().rewards.find_one(sort=[("_id", pymongo.DESCENDING)])
        return defaultValue if lastSyncedRewardEpochReward is None else lastSyncedRewardEpochReward["_id"]

    def getBurnedRewardAmount(self):
        query = list(self.instance().rewards.aggregate([
            {"$group": {"_id": "null", "amount": {"$sum": "$burnedReward"}}}
        ]))
        return 0 if len(query) == 0 else query[0]["amount"]

    def insertRewards(self, rewards):
        self.instance().rewards.insert_many(rewards)

    """
    ### Swaps
    """

    def getLastSyncedSwapTimestamp(self, defaultValue):
        lastSyncedSwap = self.instance().swaps.find_one(sort=[("timestamp", pymongo.DESCENDING)])
        return defaultValue if lastSyncedSwap is None else lastSyncedSwap["timestamp"]

    def getAllSwaps(self):
        return list(self.instance().swaps.find())

    def insertSwaps(self, swaps):
        self.instance().swaps.insert_many(swaps)

    """
    ### ERC20Transfers
    """

    def getLastSyncedERC20TransferBlockHeight(self, defaultValue):
        lastSyncedERC20Transfer = self.instance().erc20_transfers.find_one(sort=[("block", pymongo.DESCENDING)])
        return defaultValue if lastSyncedERC20Transfer is None else lastSyncedERC20Transfer["block"]

    def getAllERC20Transfers(self):
        return list(self.instance().erc20_transfers.find())

    def insertERC20Transfers(self, transfers):
        self.instance().erc20_transfers.insert_many(transfers)

    """
    ### BEP2Transfers
    """

    def getLastSyncedBEP2TransferTimestamp(self, defaultValue):
        lastSyncedBEP2Transfer = self.instance().bep2_transfers.find_one(sort=[("timestamp", pymongo.DESCENDING)])
        return defaultValue if lastSyncedBEP2Transfer is None else lastSyncedBEP2Transfer["timestamp"]

    def getAllBEP2Transfers(self):
        return list(self.instance().bep2_transfers.find())

    def insertBEP2Transfers(self, transfers):
        self.instance().bep2_transfers.insert_many(transfers)

    ##################################################################################################################################################

    """
    ### API
    """

    def getValidators(self, hideUnknown, sortKey, sortOrder):
        query = {"name": {"$ne": ""}} if hideUnknown == "true" else {}
        validators = self.instance().validators.find(query).sort(sortKey, pymongo.ASCENDING if sortOrder == "asc" else pymongo.DESCENDING)
        return list(validators)
