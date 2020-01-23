from queue import Queue
from threading import Thread


class Delegations:
    __list = []

    def __init__(self, sfc, db):
        self.__sfc = sfc
        self.__db = db

    def __fetchDelegation(self, addressQueue):
        while True:
            address = addressQueue.get()
            delegation = self.__sfc.getDelegations(address)

            self.__list += [{
                "address": address,
                "delegation": delegation
            }]

            addressQueue.task_done()

    def getAll(self):
        return self.__list

    def update(self, delegatorAddresses):
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

        # Update delegations
        self.__db.table("delegations").insert_multiple(self.__list)
