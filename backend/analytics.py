from modules.Database import Database


database = Database()
swaps = database.getAllSwaps()

#####

toFtm = list(filter(lambda swap: swap["destination"] == "FTM", swaps))
toFtmSum = sum(map(lambda swap: swap["amount"], toFtm))
toFtmFromEthSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "ETH", toFtm)))
toFtmFromBnbSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "BNB", toFtm)))
toFtmFromXarSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "XAR", toFtm)))

fromFtm = list(filter(lambda swap: swap["source"] == "FTM", swaps))
fromFtmSum = sum(map(lambda swap: swap["amount"], fromFtm))
fromFtmToEthSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "ETH", fromFtm)))
fromFtmToBnbSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "BNB", fromFtm)))
fromFtmToXarSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "XAR", fromFtm)))

ftmNet = toFtmSum - fromFtmSum
ftmEthNet = toFtmFromEthSum - fromFtmToEthSum
ftmBnbNet = toFtmFromBnbSum - fromFtmToBnbSum
ftmXarNet = toFtmFromXarSum - fromFtmToXarSum

#####

toEth = list(filter(lambda swap: swap["destination"] == "ETH", swaps))
toEthSum = sum(map(lambda swap: swap["amount"], toEth))
toEthFromFtmSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "FTM", toEth)))
toEthFromBnbSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "BNB", toEth)))
toEthFromXarSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "XAR", toEth)))

fromEth = list(filter(lambda swap: swap["source"] == "ETH", swaps))
fromEthSum = sum(map(lambda swap: swap["amount"], fromEth))
fromEthToFtmSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "FTM", fromEth)))
fromEthToBnbSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "BNB", fromEth)))
fromEthToXarSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "XAR", fromEth)))

ethNet = toEthSum - fromEthSum
ethFtmNet = toEthFromFtmSum - fromEthToFtmSum
ethBnbNet = toEthFromBnbSum - fromEthToBnbSum
ethXarNet = toEthFromXarSum - fromEthToXarSum

#####

toBnb = list(filter(lambda swap: swap["destination"] == "BNB", swaps))
toBnbSum = sum(map(lambda swap: swap["amount"], toBnb))
toBnbFromFtmSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "FTM", toBnb)))
toBnbFromEthSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "ETH", toBnb)))
toBnbFromXarSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "XAR", toBnb)))

fromBnb = list(filter(lambda swap: swap["source"] == "BNB", swaps))
fromBnbSum = sum(map(lambda swap: swap["amount"], fromBnb))
fromBnbToFtmSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "FTM", fromBnb)))
fromBnbToEthSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "ETH", fromBnb)))
fromBnbToXarSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "XAR", fromBnb)))

bnbNet = toBnbSum - fromBnbSum
bnbFtmNet = toBnbFromFtmSum - fromBnbToFtmSum
bnbEthNet = toBnbFromEthSum - fromBnbToEthSum
bnbXarNet = toBnbFromXarSum - fromBnbToXarSum

#####

toXar = list(filter(lambda swap: swap["destination"] == "XAR", swaps))
toXarSum = sum(map(lambda swap: swap["amount"], toXar))
toXarFromFtmSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "FTM", toXar)))
toXarFromEthSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "ETH", toXar)))
toXarFromBnbSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["source"] == "BNB", toXar)))

fromXar = list(filter(lambda swap: swap["source"] == "XAR", swaps))
fromXarSum = sum(map(lambda swap: swap["amount"], fromXar))
fromXarToFtmSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "FTM", fromXar)))
fromXarToEthSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "ETH", fromXar)))
fromXarToBnbSum = sum(map(lambda swap: swap["amount"], filter(lambda swap: swap["destination"] == "BNB", fromXar)))

xarNet = toXarSum - fromXarSum
xarFtmNet = toXarFromFtmSum - fromXarToFtmSum
xarEthNet = toXarFromEthSum - fromXarToEthSum
xarBnbNet = toXarFromBnbSum - fromXarToBnbSum

#####

distribution = {
    "FTM": {
        "ETH": {
            "in": toFtmFromEthSum,
            "out": fromFtmToEthSum,
            "net": ftmEthNet
        },
        "BNB": {
            "in": toFtmFromBnbSum,
            "out": fromFtmToBnbSum,
            "net": ftmBnbNet
        },
        "XAR": {
            "in": toFtmFromXarSum,
            "out": fromFtmToXarSum,
            "net": ftmXarNet
        },
        "balance": ftmEthNet + ftmBnbNet + ftmXarNet
    },
    "ETH": {
        "FTM": {
            "in": toEthFromFtmSum,
            "out": fromEthToFtmSum,
            "net": ethFtmNet
        },
        "BNB": {
            "in": toEthFromBnbSum,
            "out": fromEthToBnbSum,
            "net": ethBnbNet
        },
        "XAR": {
            "in": toEthFromXarSum,
            "out": fromEthToXarSum,
            "net": ethXarNet
        },
        "balance": ethFtmNet + ethBnbNet + ethXarNet
    },
    "BNB": {
        "FTM": {
            "in": toBnbFromFtmSum,
            "out": fromBnbToFtmSum,
            "net": bnbFtmNet
        },
        "ETH": {
            "in": toBnbFromEthSum,
            "out": fromBnbToEthSum,
            "net": bnbEthNet
        },
        "XAR": {
            "in": toBnbFromXarSum,
            "out": fromBnbToXarSum,
            "net": bnbXarNet
        },
        "balance": bnbFtmNet + bnbEthNet + bnbXarNet
    },
    "XAR": {
        "FTM": {
            "in": toXarFromFtmSum,
            "out": fromXarToFtmSum,
            "net": xarFtmNet
        },
        "ETH": {
            "in": toXarFromEthSum,
            "out": fromXarToEthSum,
            "net": xarEthNet
        },
        "BNB": {
            "in": toXarFromBnbSum,
            "out": fromXarToBnbSum,
            "net": xarBnbNet
        },
        "balance": xarFtmNet + xarEthNet + xarBnbNet
    }
}

x = 3