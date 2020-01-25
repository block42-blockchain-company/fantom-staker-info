class EpochRewards:
    def __init__(self, sfc, db, epochs, delegations):
        self.__sfc = sfc
        self.__db = db
        self.__epochs = epochs
        self.__delegations = delegations
        self.__activeDelegations = list(filter(lambda delegation: delegation["data"][3] == 0, self.__delegations))
        self.__data = []

    def getAll(self):
        return self.__data + self.__db.table("rewards").all() if len(self.__data) != 0 else self.__db.table("rewards").all()

    def sync(self):
        latestSyncedRewardEpochId = 0 if len(self.getAll()) == 0 else max(self.getAll(), key=lambda epochReward: epochReward["epochId"])["epochId"]
        epochs = sorted(self.__epochs, key=lambda epoch: epoch["id"], reverse=False)[latestSyncedRewardEpochId:]

        for epoch in epochs:
            epochId = epoch["id"]

            duration = epoch["data"][1]
            fee = epoch["data"][2]
            totalBaseRewardWeight = epoch["data"][3]
            totalTxRewardWeight = epoch["data"][4]
            baseRewardPerSecond = epoch["data"][5]

            epochDelegationReward = 0
            epochValidationReward = 0
            epochContractCommission = 0

            for validator in epoch["validators"]:
                baseRewardWeight = validator["data"][2]
                txRewardWeight = validator["data"][3]

                # Calculate epoch reward
                baseReward = duration * baseRewardPerSecond * (baseRewardWeight / totalBaseRewardWeight)
                txReward = 0 if totalTxRewardWeight == 0 else fee * (txRewardWeight / totalTxRewardWeight) * 0.7
                totalReward = baseReward + txReward

                # Calculate epoch validation reward
                validatorStake = validator["data"][0]
                validatorDelegated = validator["data"][1]
                validatorTotalStaked = validatorStake + validatorDelegated
                weightedValidatorStake = validatorStake + validatorDelegated * 0.15  # Add 15% validation fee
                epochValidationReward += 0 if validatorTotalStaked == 0 else ((totalReward * (weightedValidatorStake / validatorTotalStaked)) / 1e18)

                # Calculate epoch delegation reward
                delegationsOfEpoch = list(filter(lambda delegation: delegation["data"][0] == epochId, self.__activeDelegations))
                delegationAmount = sum(map(lambda delegation: delegation["data"][4], delegationsOfEpoch))
                weightedDelegationAmount = delegationAmount * 0.85  # Subtract 15% validation fee
                epochDelegationReward += 0 if validatorTotalStaked == 0 else ((totalReward * (weightedDelegationAmount / validatorTotalStaked)) / 1e18)

                # Calculate epoch contract commission
                epochContractCommission += (((txReward / 0.7) * 0.3) / 1e18)  # 30% of tx fees

            self.__data += [{
                "epochId": epochId,
                "delegationReward": epochDelegationReward,
                "validationReward": epochValidationReward,
                "contractCommission": epochContractCommission
            }]

        return self

    def save(self):
        self.__db.table("rewards").insert_multiple(self.__data)
