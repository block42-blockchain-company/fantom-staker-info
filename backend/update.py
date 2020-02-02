from datetime import datetime

from modules.Database import Database
from modules.FantomRPC import FantomRPC
from modules.Web3Client import Web3Client as Web3

from modules.StakersContract import StakersContract
from modules.StakerInfoContract import StakerInfoContract

from modules.Epochs import Epochs
from modules.Events import Events
from modules.Blocks import Blocks
from modules.Transactions import Transactions
from modules.Delegations import Delegations
from modules.Validators import Validators
from modules.Rewards import Rewards


web3 = Web3()
rpc = FantomRPC()
database = Database()

sfcContract = StakersContract(web3=web3)
stakerInfoContract = StakerInfoContract(web3=web3)

# Sync epochs
print("Syncing epochs ...")
epochs = Epochs(sfcContract=sfcContract, database=database).sync()
epochs.save()

# Sync events
print("Syncing events ...")
events = Events(rpc=rpc, database=database).sync()
events.save()

# Sync blocks
print("Syncing blocks ...")
blocks = Blocks(web3=web3, database=database).sync()
blocks.save()

# Sync transactions
print("Syncing transactions ...")
transactions = Transactions(web3=web3, database=database).sync()
transactions.save()

# Sync delegations
print("Syncing delegations ...")
delegations = Delegations(sfcContract=sfcContract, database=database).sync()
delegations.save()

# Sync validators
validators = Validators(sfcContract=sfcContract, stakerInfoContract=stakerInfoContract, database=database)
print("Syncing validators ...")
for validatorId in range(1, sfcContract.getValidatorCount() + 1):
    print("Syncing validator #" + str(validatorId) + " ...")
    validators.sync(validatorId=validatorId)

# Sync epoch rewards
print("Syncing epoch rewards ...")
rewards = Rewards(sfcContract=sfcContract, database=database).sync()
rewards.save()

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
    "lastUpdated": datetime.now().timestamp()
})
