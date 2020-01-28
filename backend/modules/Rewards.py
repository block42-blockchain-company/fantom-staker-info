class Rewards:
    def __init__(self, sfcContract, database):
        self.__sfcContract = sfcContract
        self.__database = database
        self.__data = []

    def sync(self):
        latestSyncedRewardEpochId = self.__database.getLastSyncedRewardEpochId(defaultValue=0)
        epochs = self.__database.getAllEpochs()
        epochs = sorted(epochs, key=lambda epoch: epoch["_id"], reverse=False)[latestSyncedRewardEpochId:]

        for epoch in epochs:
            epochId = epoch["_id"]

            print("Calculating epoch #" + str(epochId) + " rewards ...")

            duration = epoch["data"]["duration"]
            epochFee = epoch["data"]["epochFee"]
            totalBaseRewardWeight = epoch["data"]["totalBaseRewardWeight"]
            totalTxRewardWeight = epoch["data"]["totalTxRewardWeight"]
            baseRewardPerSecond = epoch["data"]["baseRewardPerSecond"]

            # Get epoch delegations
            activeEpochDelegations = self.__database.getAllActiveEpochDelegations(epochId=epochId)
            inactiveEpochDelegations = self.__database.getAllInactiveEpochDelegations(epochId=epochId)

            epochValidationReward = 0
            epochDelegationReward = 0
            epochDelegationRewardBurned = 0
            epochContractCommission = 0

            for validator in epoch["validators"]:
                validatorId = validator["id"]

                baseRewardWeight = validator["data"]["baseRewardWeight"]
                txRewardWeight = validator["data"]["txRewardWeight"]

                # Calculate epoch reward
                baseReward = duration * baseRewardPerSecond * (baseRewardWeight / totalBaseRewardWeight)
                txReward = 0 if totalTxRewardWeight == 0 else epochFee * (txRewardWeight / totalTxRewardWeight) * 0.7
                totalReward = baseReward + txReward

                # Calculate epoch validation reward
                validatorStake = validator["data"]["stakeAmount"]
                validatorDelegated = validator["data"]["delegatedMe"]
                validatorTotalStaked = validatorStake + validatorDelegated
                weightedValidatorStake = validatorStake + validatorDelegated * 0.15  # Add 15% validation fee
                epochValidationReward += 0 if validatorTotalStaked == 0 else (totalReward * (weightedValidatorStake / validatorTotalStaked))

                # Calculate epoch delegation reward
                activeDelegations = list(filter(lambda delegation: delegation["validatorId"] == validatorId, activeEpochDelegations))
                activeDelegationAmount = sum(map(lambda delegation: delegation["amount"], activeDelegations))
                activeWeightedDelegationAmount = activeDelegationAmount * 0.85  # Subtract 15% validation fee
                epochDelegationReward += 0 if validatorTotalStaked == 0 else (totalReward * (activeWeightedDelegationAmount / validatorTotalStaked))

                # Calculate burned epoch delegation reward
                inactiveDelegations = list(filter(lambda delegation: delegation["validatorId"] == validatorId, inactiveEpochDelegations))
                inactiveDelegationAmount = sum(map(lambda delegation: delegation["amount"], inactiveDelegations))
                inactiveWeightedDelegationAmount = inactiveDelegationAmount * 0.85  # Subtract 15% validation fee
                epochDelegationRewardBurned += 0 if validatorTotalStaked == 0 else (totalReward * (inactiveWeightedDelegationAmount / validatorTotalStaked))

                # Calculate epoch contract commission
                epochContractCommission += ((txReward / 0.7) * 0.3)  # 30% of tx fees

            self.__data += [{
                "_id": epochId,
                "validationReward": epochValidationReward,
                "delegationReward": epochDelegationReward,
                "burnedReward": epochDelegationRewardBurned,
                "contractCommission": epochContractCommission
            }]

        return self

    def save(self):
        if len(self.__data) != 0:
            self.__database.insertRewards(rewards=self.__data)
