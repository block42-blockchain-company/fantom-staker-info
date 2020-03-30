import json
import moment
import requests

from Crypto.Hash import SHA256


def hexEncode(string: str):
    return ''.join(list(map(lambda character: hex(ord(character))[2:].zfill(4), string)))


class Swaps:
    def __init__(self, database):
        self.__database = database
        self.__data = []

    def sync(self):
        mnemonic = "task garage suffer tape salon envelope steak melody neutral comfort design rose"
        encryptedPayload = "qitcGwcHFk6jhBlZkSXQOVr3Ox6OUBc3P33K0bJpk+JzCP+PKHzslR3AWuAy9YKyoIIs/tRmAcOJSqJdlHtsyg=="
        url = "/api/v1/getTransfers"

        data = {
            "e": hexEncode(encryptedPayload),
            "m": hexEncode(mnemonic),
            "u": SHA256.new(url.encode()).hexdigest().upper(),
            "p": SHA256.new(SHA256.new(url.encode()).hexdigest().upper().encode()).hexdigest().upper(),
            "t": int(moment.now().datetime.timestamp() * 1000)
        }
        data["s"] = SHA256.new(json.dumps(data).replace(" ", "").encode()).hexdigest()

        lastSyncedSwapTimestamp = self.__database.getLastSyncedSwapTimestamp(defaultValue=0)

        transfers = requests.post(url="https://api.bnbridge.exchange/api/v1/getTransfers", json=data).json()["result"]["transfers"]
        transfers = list(map(lambda transfer: {
                "_id": transfer["uuid"],
                "amount": float(transfer["amount"]),
                "timestamp": int(moment.date(transfer["created"]).datetime.timestamp()),
                "source": self.getTickerFromNetworkString(networkString=transfer["direction"].split("To")[0]),
                "sourceTxHash": transfer["deposit_transaction_hash"],
                "sourceFromAddress": str(transfer["client_from_address"]).lower(),
                "sourceToAddress": str(transfer["client_to_address"]).lower(),
                "destination": self.getTickerFromNetworkString(networkString=transfer["direction"].split("To")[1]),
                "destinationTxHash": transfer["transfer_transaction_hash"],
                "destinationFromAddress": str(transfer["server_from_address"]).lower(),
                "destinationToAddress": str(transfer["server_to_address"]).lower()
            }, transfers))

        transfers = list(filter(lambda transfer: transfer["timestamp"] > lastSyncedSwapTimestamp, transfers))

        for transfer in transfers:
            swap = transfer

            # Sanity check (for some reason swap amounts coming from XAR network might be too large by 10e6)
            swap["amount"] = swap["amount"] / (10 ** 6) if swap["source"] == "XAR" and swap["amount"] > (10 * 10 ** 6) else swap["amount"]

            print("Syncing swap " + swap["_id"] + " (" + str(round(swap["amount"], 2)) + " from " + swap["source"] + " to " + swap["destination"] + ") ...")

            self.__data += [swap]

        # Save to database
        if len(self.__data) != 0:
            self.__database.insertSwaps(swaps=self.__data)

        return self

    @staticmethod
    def getTickerFromNetworkString(networkString):
        if networkString == "Opera":
            ticker = "FTM"
        elif networkString == "Fantom":
            ticker = "XAR"
        elif networkString == "Ethereum":
            ticker = "ETH"
        elif networkString == "Binance":
            ticker = "BNB"
        else:
            raise ValueError("Unknown network: " + networkString)

        return ticker
