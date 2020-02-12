import json
import base64
import moment
import requests
import binascii

from mnemonic import Mnemonic

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding
from Crypto.Protocol.KDF import PBKDF2


class Swaps:
    def __init__(self, database):
        self.__database = database
        self.__data = []

    def sync(self):
        """
function encrypt(data, url) {
  const signJson = JSON.stringify(data);
  const signMnemonic = bip39.generateMnemonic();
  const cipher = crypto.createCipher('aes-256-cbc', signMnemonic);
  const signEncrypted =
    cipher.update(signJson, 'utf8', 'base64') + cipher.final('base64');
  var signData = {
    e: signEncrypted.hexEncode(),
    m: signMnemonic.hexEncode(),
    u: sha256(url).toUpperCase(),
    p: sha256(sha256(url).toUpperCase()).toUpperCase(),
    t: new Date().getTime()
  };
  const signSeed = JSON.stringify(signData);
  const signSignature = sha256(signSeed);
  signData.s = signSignature;
  return JSON.stringify(signData);
}
        :return:
        """

        signJson = json.dumps({"token_uuid": "133f21df-9a2c-0a65-b532-d5df78b92c26"})

        signMnemonic = Mnemonic("english").generate()

        salt = Random.get_random_bytes(32)
        key = PBKDF2(signMnemonic, salt, dkLen=32)
        iv = Random.new().read(AES.block_size)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        signEncrypted = base64.b64encode(iv + cipher.encrypt(Padding.pad(signJson.encode(), AES.block_size)))

        url = "/api/v1/getTransfers"

        signData = {
            "e": str(binascii.hexlify(signEncrypted), "utf-8"),
            "m": str(binascii.hexlify(signMnemonic.encode()), "utf-8"),
            "u": SHA256.new(url.encode()).hexdigest().upper(),
            "t": int(moment.now().datetime.timestamp() * 1000),
            "p": SHA256.new(SHA256.new(url.encode()).hexdigest().encode()).hexdigest().upper()
        }

        signSeed = json.dumps(signData)
        signSignature = SHA256.new(signSeed.encode()).hexdigest()
        signData["s"] = signSignature

        sig = {
            "e": signData["e"],
            "m": signData["m"],
            "u": signData["u"],
            "t": signData["t"],
            "p": signData["p"]
        }
        seed = json.dumps(sig)
        signCompare = SHA256.new(seed.encode()).hexdigest()

        transfers = requests.post(url="https://api.bnbridge.exchange/api/v1/getTransfers", json=signData).json()["result"]["transfers"]

        for transfer in transfers:
            swap = {
                "_id": transfer["uuid"],
                "amount": float(transfer["amount"]),
                "timestamp": moment.date(transfer["created"]).datetime,
                "source": self.getTickerFromNetworkString(networkString=transfer["direction"].split("To")[0]),
                "sourceTxHash": transfer["deposit_transaction_hash"],
                "sourceFromAddress": transfer["client_from_address"],
                "sourceToAddress": transfer["client_to_address"],
                "destination": self.getTickerFromNetworkString(networkString=transfer["direction"].split("To")[1]),
                "destinationTxHash": transfer["transfer_transaction_hash"],
                "destinationFromAddress": transfer["server_from_address"],
                "destinationToAddress": transfer["server_to_address"]
            }

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
            raise ValueError("Unknown network for swap")

        return ticker
