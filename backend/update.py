from datetime import datetime

from modules.Database import Database
from modules.Web3Client import Web3Client as Web3

from modules.StakersContract import StakersContract
from modules.StakerInfoContract import StakerInfoContract

from modules.Validators import Validators
from modules.Delegators import Delegators
from modules.Delegations import Delegations
from modules.Epochs import Epochs
from modules.EpochRewards import EpochRewards


web3 = Web3().instance()
database = Database().instance()

sfcContract = StakersContract(web3=web3)
stakerInfoContract = StakerInfoContract(web3=web3)

validators = Validators(sfc=sfcContract, stakerInfo=stakerInfoContract, db=database)
delegators = Delegators(db=database)

# Sync delegators
for validatorId in range(1, sfcContract.getValidatorCount() + 1):
    delegators.sync(validatorId=validatorId)

# Sync delegations
delegatorAddresses = sum([validator["delegators"] for validator in delegators.getAll()], [])
delegations = Delegations(sfc=sfcContract, db=database).sync(delegatorAddresses=delegatorAddresses)

# Sync validators
for validatorId in range(1, sfcContract.getValidatorCount() + 1):
    validators.sync(validatorId=validatorId, deactivatedDelegations=delegations.getDeactivated(validatorId=validatorId))

# Sync epochs
epochs = Epochs(sfc=sfcContract, db=database).sync()

# Sync epoch rewards
epochRewards = EpochRewards(sfc=sfcContract, db=database, epochs=epochs.getAll(), delegations=delegations.getAll()).sync()

# Calculate totals
totalSelfStakedSum = sum(validator["selfStakedAmount"] for validator in validators.getAll())
totalDelegatedSum = sum(validator["delegatedAmount"] for validator in validators.getAll())
totalInUndelegationSum = sum(validator["inUndelegationAmount"] for validator in validators.getAll())
totalStakedSum = totalSelfStakedSum + totalDelegatedSum + totalInUndelegationSum

# Calculate total rewards
totalDelegationRewardSum = sum(map(lambda epochReward: epochReward["delegationReward"], epochRewards.getAll()))
totalValidatorRewardSum = sum(map(lambda epochReward: epochReward["validationReward"], epochRewards.getAll()))
totalContractCommissionSum = sum(map(lambda epochReward: epochReward["contractCommission"], epochRewards.getAll()))
totalRewardSum = Web3().getBalance(address=sfcContract.getAddress()) - totalStakedSum
totalBurnedRewardSum = totalRewardSum - (totalDelegationRewardSum + totalValidatorRewardSum + totalContractCommissionSum)

# Calculate total percentages
totalSupply = sfcContract.getTotalSupply()
totalSelfStakedPercent = totalSelfStakedSum / totalSupply
totalDelegatedPercent = totalDelegatedSum / totalSupply
totalInUndelegationPercent = totalInUndelegationSum / totalSupply
totalStakedPercent = totalStakedSum / totalSupply
totalBurnedRewardPercent = totalBurnedRewardSum / totalSupply

# Set staking power
validators.setStakingPower(totalStakedSum=totalStakedSum)

# Update
database.purge_table("general")
database.table("general").insert({
    "totalSelfStakedSum": totalSelfStakedSum,
    "totalSelfStakedPercent": totalSelfStakedPercent,
    "totalDelegatedSum": totalDelegatedSum,
    "totalDelegatedPercent": totalDelegatedPercent,
    "totalInUndelegationSum": totalInUndelegationSum,
    "totalInUndelegationPercent": totalInUndelegationPercent,
    "totalStakedSum": totalStakedSum,
    "totalStakedPercent": totalStakedPercent,
    "totalBurnedRewardSum": totalBurnedRewardSum,
    "totalBurnedRewardPercent": totalBurnedRewardPercent,
    "totalSupply": totalSupply,
    "rewardUnlockDate": sfcContract.getRewardUnlockDate(),
    "rewardUnlockPercent": sfcContract.getRewardUnlockPercentage(),
    "roi": sfcContract.getRoi(),
    "lastUpdated": datetime.now().timestamp()
})

# Update
validators.save()
delegators.save()
delegations.save()
epochs.save()
epochRewards.save()