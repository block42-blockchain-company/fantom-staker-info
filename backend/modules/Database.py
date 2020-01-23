from tinydb import TinyDB


class Database:
    def __init__(self):
        self.__instance = TinyDB("./db.json")

    def instance(self):
        return self.__instance
