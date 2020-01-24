from queue import Queue
from threading import Thread

from tinydb import where


class Delegations:
    def __init__(self, sfc, db):
        self.__sfc = sfc
        self.__db = db
        self.__data = []

    def __fetchDelegation(self, addressQueue):
        while True:
            address = addressQueue.get()
            delegation = self.__sfc.getDelegations(address)

            self.__data += [{
                "address": address,
                "delegation": delegation
            }]

            addressQueue.task_done()

    def sync(self, delegatorAddresses):
        addressQueue = Queue()

        # Add addresses to queue
        for delegatorAddress in delegatorAddresses:
            addressQueue.put(delegatorAddress)

        for i in range(5):
            worker = Thread(target=self.__fetchDelegation, args=(addressQueue,))
            worker.setDaemon(True)
            worker.start()

        # Wait for all workers to finish
        addressQueue.join()

        return self

    def save(self):
        self.__db.purge_table("delegations")
        self.__db.table("delegations").insert_multiple(self.__data)

    def getAll(self):
        return self.__data

    def getAllActivate(self):
        return filter(lambda address: address["delegation"][3] == 0, self.__data)

    def getActivate(self, validatorId):
        return filter(lambda address: address["delegation"][3] == 0 and address["delegation"][6] == validatorId, self.__data)

    def getAllDeactivated(self):
        return filter(lambda address: address["delegation"][3] != 0, self.__data)

    def getDeactivated(self, validatorId):
        return filter(lambda address: address["delegation"][3] != 0 and address["delegation"][6] == validatorId, self.__data)
