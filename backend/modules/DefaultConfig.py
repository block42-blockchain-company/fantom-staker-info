class DefaultConfig:
    data = {
        13: {"name": "Fantom Vietnam", "website": "https://fantomviet.com"},
        15: {"name": "Fantom Validator", "website": "https://www.fantomvalidator.com"},
        16: {"name": "bu1137", "website": "https://keybase.io/nickai"},
        17: {"name": "GoFantom", "website": "https://gofantom.net"},
        18: {"name": "GoStake Network", "website": "https://gostake.com"},
        19: {"name": "Fantom Ukraine", "website": ""},
        20: {"name": "Binary Fintech Group", "website": "http://binaryfin.com"},
        21: {"name": "Fantom Global", "website": "https://fantom.global"},
        22: {"name": "Fantom Russian", "website": ""},
        24: {"name": "lopalcar", "website": "https://fantomstakers.com"},
        27: {"name": "Cryptoast.io", "website": "https://cryptoast.io"},
        28: {"name": "Hyperblocks", "website": "https://hyperblocks.pro"}
    }

    @staticmethod
    def containsInfoForValidator(validatorId):
        return validatorId in DefaultConfig.data

    @staticmethod
    def getInfoForValidator(validatorId):
        return DefaultConfig.data[validatorId]
