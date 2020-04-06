from datetime import datetime

from modules.Database import Database
from modules.FantomApi import FantomApi
from modules.EthereumApi import EthereumApi
from modules.BinanceApi import BinanceApi

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
from modules.ERC20Transfers import ERC20Transfers
from modules.BEP2Transfers import BEP2Transfers


class App:
    @staticmethod
    def run():
        database = Database()
        fantomApi = FantomApi()
        ethereumApi = EthereumApi()
        binanceApi = BinanceApi()

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
        Blocks(sfcContract=sfcContract, fantomApi=fantomApi, database=database).sync()

        # Sync transactions
        print("Syncing transactions ...")
        Transactions(fantomApi=fantomApi, database=database).sync()

        # Sync delegations
        print("Syncing delegations ...")
        Delegations(sfcContract=sfcContract, database=database).sync()

        # Sync epoch rewards
        print("Syncing epoch rewards ...")
        Rewards(sfcContract=sfcContract, database=database).sync()

        # Sync ERC20 transfers
        print("Syncing ERC20 transfers ...")
        ERC20Transfers(ethereumApi=ethereumApi, database=database).sync()

        # Sync BEP2 transfers
        print("Syncing BEP2 transfers ...")
        BEP2Transfers(binanceApi=binanceApi, database=database).sync()

        # Sync swaps
        print("Syncing swaps ...")
        Swaps(database=database).sync()

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
        totalStakedSum = totalSelfStakedSum + totalDelegatedSum
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

        # Get staking roi
        roi = sfcContract.getRoi(totalStaked=totalSelfStakedSum, totalDelegated=totalDelegatedSum)

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
            "roi": roi * 0.85,  # 15% validator fee
            "validatorRoi": roi,
            "lastUpdated": int(datetime.now().timestamp())
        })
