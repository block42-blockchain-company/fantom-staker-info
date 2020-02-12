from datetime import datetime

from modules.Database import Database
from modules.FantomApi import FantomApi

from modules.StakersContract import StakersContract
from modules.StakerInfoContract import StakerInfoContract

from modules.Epochs import Epochs
from modules.Events import Events
from modules.Blocks import Blocks
from modules.Transactions import Transactions
from modules.Delegations import Delegations
from modules.Validators import Validators
from modules.Rewards import Rewards
from modules.Swaps import Swaps


database = Database()
fantomApi = FantomApi()

sfcContract = StakersContract(fantomApi=fantomApi)
stakerInfoContract = StakerInfoContract(fantomApi=fantomApi)

# Sync epochs
print("Syncing epochs ...")
Epochs(sfcContract=sfcContract, database=database).sync()

# Sync events
print("Syncing events ...")
Events(fantomApi=fantomApi, database=database).sync()

# Sync blocks
print("Syncing blocks ...")
Blocks(fantomApi=fantomApi, database=database).sync()

# Sync transactions
print("Syncing transactions ...")
Transactions(fantomApi=fantomApi, database=database).sync()

# Sync delegations
print("Syncing delegations ...")
Delegations(sfcContract=sfcContract, database=database).sync()

# Sync epoch rewards
print("Syncing epoch rewards ...")
Rewards(sfcContract=sfcContract, database=database).sync()

# Sync swaps
#print("Syncing swaps ...")
#Swaps(database=database).sync()

# Sync validators
validators = Validators(sfcContract=sfcContract, stakerInfoContract=stakerInfoContract, database=database)
print("Syncing validators ...")
for validatorId in range(1, sfcContract.getValidatorCount() + 1):
    print("Syncing validator #" + str(validatorId) + " ...")
    validators.sync(validatorId=validatorId)

# Calculate totals
totalSelfStakedSum = sum(validator["selfStakedAmount"] for validator in validators.getAll())
totalDelegatedSum = sum(validator["delegatedAmount"] for validator in validators.getAll())
totalInUndelegationSum = sum(validator["inUndelegationAmount"] for validator in validators.getAll())
totalStakedSum = totalSelfStakedSum + totalDelegatedSum + totalInUndelegationSum
totalBurnedRewardSum = database.getBurnedRewardAmount()

# Calculate total percentages
totalSupply = sfcContract.getTotalSupply()
totalSelfStakedPercent = totalSelfStakedSum / totalSupply
totalDelegatedPercent = totalDelegatedSum / totalSupply
totalInUndelegationPercent = totalInUndelegationSum / totalSupply
totalStakedPercent = totalStakedSum / totalSupply
totalBurnedRewardPercent = totalBurnedRewardSum / totalSupply

# Set staking power
validators.setStakingPower(totalStakedSum=totalStakedSum)
validators.save()

# Update
database.instance().general.drop()
database.instance().general.insert_one({
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
    "lastUpdated": int(datetime.now().timestamp())
})
