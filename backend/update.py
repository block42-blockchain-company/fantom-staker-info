from datetime import datetime

from modules.Database import Database
from modules.Web3Client import Web3Client as Web3

from modules.StakersContract import StakersContract
from modules.StakerInfoContract import StakerInfoContract

from modules.Validators import Validators
from modules.Delegators import Delegators
from modules.Epochs import Epochs
from modules.Delegations import Delegations

web3 = Web3().instance()
database = Database().instance()

sfcContract = StakersContract(web3=web3)
stakerInfoContract = StakerInfoContract(web3=web3)

validators = Validators(sfc=sfcContract, stakerInfo=stakerInfoContract, db=database)
delegators = Delegators(db=database)

# Update delegators
for validatorId in range(1, sfcContract.getValidatorCount() + 1):
    delegators.add(validatorId)

# Update delegations
delegatorAddresses = sum([validator["delegators"] for validator in delegators.getAll()], [])
delegations = Delegations(sfc=sfcContract, db=database)
delegations.update(delegatorAddresses)

# Update validators
for validatorId in range(1, sfcContract.getValidatorCount() + 1):
    validators.add(validatorId, deactivatedDelegations=delegations.getDeactivated(validatorId))

# Calculate totals
totalSelfStakedSum = sum(validator["selfStakedAmount"] for validator in validators.getAll())
totalDelegatedSum = sum(validator["delegatedAmount"] for validator in validators.getAll())
totalInUndelegationSum = sum(validator["inUndelegationAmount"] for validator in validators.getAll())
totalStakedSum = totalSelfStakedSum + totalDelegatedSum + totalInUndelegationSum

# Calculate total percentages
totalSupply = sfcContract.getTotalSupply()
totalSelfStakedPercent = totalSelfStakedSum / totalSupply
totalDelegatedPercent = totalDelegatedSum / totalSupply
totalInUndelegationPercent = totalInUndelegationSum / totalSupply
totalStakedPercent = totalStakedSum / totalSupply

# Update epochs
epochs = Epochs(sfc=sfcContract, db=database)
epochs.update()

# Update general info
database.table("general").insert({
    "totalSelfStakedSum": totalSelfStakedSum,
    "totalDelegatedSum": totalDelegatedSum,
    "totalInUndelegationSum": totalInUndelegationSum,
    "totalStakedSum": totalStakedSum,
    "totalSelfStakedPercent": totalSelfStakedPercent,
    "totalDelegatedPercent": totalDelegatedPercent,
    "totalInUndelegationPercent": totalInUndelegationPercent,
    "totalStakedPercent": totalStakedPercent,
    "circulatingSupply": totalSupply,
    "rewardUnlockDate": sfcContract.getRewardUnlockDate(),
    "rewardUnlockPercent": sfcContract.getRewardUnlockPercentage(),
    "roi": sfcContract.getRoi(),
    "lastUpdated": int(datetime.now().timestamp())
})