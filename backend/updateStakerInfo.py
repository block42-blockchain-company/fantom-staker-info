import json
import urllib.request

from tinydb import TinyDB
from web3 import Web3

bootstrapInfoMap = {
    13: {
        "name": "Fantom Vietnam",
        "website": "https://fantomviet.com",
    },
    15: {
        "name": "Fantom Validator",
        "website": "https://www.fantomvalidator.com",
    },
    16: {
        "name": "bu1137",
        "website": "https://keybase.io/nickai",
    },
    17: {
        "name": "GoFantom",
        "website": "https://gofantom.net",
    },
    18: {
        "name": "GoStake Network",
        "website": "https://gostake.com",
    },
    19: {
        "name": "Fantom Ukraine",
        "website": "",
    },
    20: {
        "name": "Binary Fintech Group",
        "website": "http://binaryfin.com",
    },
    21: {
        "name": "Fantom Global",
        "website": "https://fantom.global",
    },
    22: {
        "name": "Fantom Russian",
        "website": "",
    },
    24: {
        "name": "lopalcar",
        "website": "https://fantomstakers.com",
    },
    27: {
        "name": "Cryptoast.io",
        "website": "https://cryptoast.io",
    },
    28: {
        "name": "Hyperblocks",
        "website": "https://hyperblocks.pro",
    }
}

stakerInfos = []


def parseConfig(configUrl):
    response = urllib.request.urlopen(configUrl)

    if response.code != 200:
        return "", "", "", "", False

    config = json.loads(response.read().decode())

    name = ""
    logoUrl = ""
    website = ""
    contact = ""

    for key, value in config.items():
        if key == 'name':
            name = value
        elif key == 'website':
            website = value
        elif key == 'contact':
            contact = value
        elif key == 'logoUrl':
            logoUrl = value

    return name, logoUrl, website, contact, True


# Init web3
web3 = Web3(Web3.HTTPProvider("https://rpc.fantom.network"))

# SFC Smart Contract
sfcABI = json.loads(
    '[{"constant":true,"inputs":[],"name":"minDelegation","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"bondedRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"stakersNum","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"slashedStakeTotalAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"short","type":"uint256"},{"internalType":"uint256","name":"long","type":"uint256"}],"name":"updateGasPowerAllocationRate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"withdrawDelegation","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"updateBaseRewardPerSec","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"prepareToWithdrawDelegation","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"delegationLockPeriodEpochs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"epochSnapshots","outputs":[{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"duration","type":"uint256"},{"internalType":"uint256","name":"epochFee","type":"uint256"},{"internalType":"uint256","name":"totalBaseRewardWeight","type":"uint256"},{"internalType":"uint256","name":"totalTxRewardWeight","type":"uint256"},{"internalType":"uint256","name":"baseRewardPerSecond","type":"uint256"},{"internalType":"uint256","name":"stakeTotalAmount","type":"uint256"},{"internalType":"uint256","name":"delegationsTotalAmount","type":"uint256"},{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maxDelegatedRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"contractCommission","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"delegationsTotalAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"updateStakerMetadata","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"stakerID","type":"uint256"},{"internalType":"uint256","name":"epoch","type":"uint256"}],"name":"calcTotalReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minStake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[],"name":"updateCapReachedDate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"unbondingUnlockPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"stakeTotalAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"capReachedDate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"stakeLockPeriodTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"delegationsNum","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"unbondingStartDate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"stakeLockPeriodEpochs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"addr","type":"address"}],"name":"getStakerID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"bondedTargetRewardUnlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"unbondingPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"currentSealedEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"stakersLastID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rewardsAllowed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"stakerID","type":"uint256"},{"internalType":"uint256","name":"_fromEpoch","type":"uint256"},{"internalType":"uint256","name":"maxEpochs","type":"uint256"}],"name":"calcValidatorRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakerMetadata","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"slashedDelegationsTotalAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"validatorCommission","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"maxStakerMetadataSize","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"delegator","type":"address"},{"internalType":"uint256","name":"_fromEpoch","type":"uint256"},{"internalType":"uint256","name":"maxEpochs","type":"uint256"}],"name":"calcDelegationRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"e","type":"uint256"},{"internalType":"uint256","name":"v","type":"uint256"}],"name":"epochValidator","outputs":[{"internalType":"uint256","name":"stakeAmount","type":"uint256"},{"internalType":"uint256","name":"delegatedMe","type":"uint256"},{"internalType":"uint256","name":"baseRewardWeight","type":"uint256"},{"internalType":"uint256","name":"txRewardWeight","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"withdrawStake","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"delegations","outputs":[{"internalType":"uint256","name":"createdEpoch","type":"uint256"},{"internalType":"uint256","name":"createdTime","type":"uint256"},{"internalType":"uint256","name":"deactivatedEpoch","type":"uint256"},{"internalType":"uint256","name":"deactivatedTime","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"paidUntilEpoch","type":"uint256"},{"internalType":"uint256","name":"toStakerID","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"to","type":"uint256"}],"name":"createDelegation","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"prepareToWithdrawStake","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"minStakeIncrease","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"createStake","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"increaseStake","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"stakerID","type":"uint256"},{"internalType":"uint256","name":"epoch","type":"uint256"},{"internalType":"uint256","name":"delegatedAmount","type":"uint256"}],"name":"calcDelegationReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"delegationLockPeriodTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"_fromEpoch","type":"uint256"},{"internalType":"uint256","name":"maxEpochs","type":"uint256"}],"name":"claimValidatorRewards","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"stakerID","type":"uint256"},{"internalType":"uint256","name":"epoch","type":"uint256"}],"name":"calcValidatorReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"_fromEpoch","type":"uint256"},{"internalType":"uint256","name":"maxEpochs","type":"uint256"}],"name":"claimDelegationRewards","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakers","outputs":[{"internalType":"uint256","name":"status","type":"uint256"},{"internalType":"uint256","name":"createdEpoch","type":"uint256"},{"internalType":"uint256","name":"createdTime","type":"uint256"},{"internalType":"uint256","name":"deactivatedEpoch","type":"uint256"},{"internalType":"uint256","name":"deactivatedTime","type":"uint256"},{"internalType":"uint256","name":"stakeAmount","type":"uint256"},{"internalType":"uint256","name":"paidUntilEpoch","type":"uint256"},{"internalType":"uint256","name":"delegatedMe","type":"uint256"},{"internalType":"address","name":"stakerAddress","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"},{"indexed":true,"internalType":"address","name":"stakerAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"CreatedStake","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"}],"name":"UpdatedStakerMetadata","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"diff","type":"uint256"}],"name":"IncreasedStake","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"toStakerID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"CreatedDelegation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fromEpoch","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"untilEpoch","type":"uint256"}],"name":"ClaimedDelegationReward","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fromEpoch","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"untilEpoch","type":"uint256"}],"name":"ClaimedValidatorReward","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"}],"name":"PreparedToWithdrawStake","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"penalty","type":"uint256"}],"name":"WithdrawnStake","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"}],"name":"PreparedToWithdrawDelegation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"stakerID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"penalty","type":"uint256"}],"name":"WithdrawnDelegation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_capReachedDate","type":"uint256"}],"name":"ChangedCapReachedDate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"UpdatedBaseRewardPerSec","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"short","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"long","type":"uint256"}],"name":"UpdatedGasPowerAllocationRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}]')
sfcAddress = web3.toChecksumAddress('0xfc00face00000000000000000000000000000000')
sfcContract = web3.eth.contract(address=sfcAddress, abi=sfcABI)

# StakerInfo Smart Contract
stakerInfoABI = json.loads(
    '[{"inputs":[{"internalType":"address","name":"_stakerContractAddress","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"stakerID","type":"uint256"}],"name":"InfoUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"constant":true,"inputs":[],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakerInfos","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_stakerContractAddress","type":"address"}],"name":"updateStakerContractAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_configUrl","type":"string"}],"name":"updateInfo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"_stakerID","type":"uint256"}],"name":"getInfo","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
stakerInfoAddress = web3.toChecksumAddress('0x92ffad75b8a942d149621a39502cdd8ad1dd57b4')
stakerInfoContract = web3.eth.contract(address=stakerInfoAddress, abi=stakerInfoABI)

# Get number of network validators
numValidators = sfcContract.functions.stakersNum().call()

# Calculate reward unlock date
unbondingStartDate = sfcContract.functions.unbondingStartDate().call()
unbondingUnlockPeriod = sfcContract.functions.unbondingUnlockPeriod().call()
rewardUnlockDate = unbondingStartDate + unbondingUnlockPeriod

# Get circulating supply from Etherscan API
etherscanAPI = "https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress=0x4e15361fd6b4bb609fa63c81a2be19d873717870"
etherscanResponse = json.loads(urllib.request.urlopen(etherscanAPI).read().decode())
circulatingSupply = int(etherscanResponse['result'])/ 1e18

# Initiate total variables
totalSelfStakedSum = 0
totalStakedSum = 0
totalDelegationSum = 0
totalUnbonding = 0

# Get infos for all validators
for stakerId in range(1, numValidators + 1):
    # Get the validator configUrl
    configUrl = stakerInfoContract.functions.stakerInfos(stakerId).call()

    name = ""
    logoUrl = ""
    website = ""
    contact = ""
    isVerified = configUrl is not ""

    if configUrl is not "":
        # Get info from config url
        (name, logoUrl, website, contact, isVerified) = parseConfig(configUrl)
    else:
        # No config in smart contract found, use bootstrap values
        if stakerId in bootstrapInfoMap:
            name = bootstrapInfoMap[stakerId]['name']
            website = bootstrapInfoMap[stakerId]['website']

    # Get the public variable stakers which includes some validator staking information
    sfcStakerInfo = sfcContract.functions.stakers(stakerId).call()

    # Calculate the total tokens staked to a validator = selfstaked + delegated
    selfStakeAmount = sfcStakerInfo[5] / 1e18
    delegationAmount = sfcStakerInfo[7] / 1e18
    totalStakedAmount = selfStakeAmount + delegationAmount

    totalSelfStakedSum += selfStakeAmount
    totalStakedSum += totalStakedAmount
    totalDelegationSum += delegationAmount

    stakingPower = totalStakedAmount / circulatingSupply

    # Calculate the available delegation amount for the validator
    availableDelegationAmount = selfStakeAmount * 15 - delegationAmount

    # Calculate the available delegation amount
    availableDelegationPercent = availableDelegationAmount / (selfStakeAmount * 15)

    # Get Deactivation Info; if deactivatedTime != 0 then it shows that a Staker has prepared to withdraw the stake
    isUnstaking = False
    if sfcStakerInfo[4] != 0:
        isUnstaking = True

    # Get additional info from fantom.network api
    stakerApiUrl = "https://api.fantom.network/api/v1/staker/id/" + str(stakerId) + "?verbosity=2"
    response = json.loads(urllib.request.urlopen(stakerApiUrl).read().decode())
    apiStakerInfo = response['data']

    isCheater = False
    delegationWithUnbondingAmount = 0

    for key, value in apiStakerInfo.items():
        if key == 'isCheater':
            isCheater = value
        if key == 'delegatedMe':
            delegationWithUnbondingAmount = int(value) / 1e18

    # Calculate current unbonding amount
    unbondingAmount = delegationWithUnbondingAmount - delegationAmount
    totalUnbonding += unbondingAmount

    stakerInfos += [{
        'id': stakerId,
        'name': name,
        'website': website,
        'contact': contact,
        'isVerified': isVerified,
        'logoUrl': logoUrl,
        'address': sfcStakerInfo[8],
        'selfStakeAmount': selfStakeAmount,
        'delegationAmount': delegationAmount,
        'totalStakedAmount': totalStakedAmount,
        'availableDelegationAmount': availableDelegationAmount,
        'isCheater': isCheater,
        'unbondingAmount': unbondingAmount,
        'isUnstaking': isUnstaking,
        'stakingPower': stakingPower
    }]


totalStakedSumPercentage = totalStakedSum / circulatingSupply
delegationCapacity = totalSelfStakedSum * 15
delegationCapacityPercentage = totalDelegationSum / delegationCapacity

general = {
    'circulatingSupply': circulatingSupply,
    'totalSelfStakedSum': totalSelfStakedSum,
    'totalDelegationSum': totalDelegationSum,
    'totalStakedSum': totalStakedSum,
    'totalStakedSumPercentage': totalStakedSumPercentage,
    'totalUnbonding': totalUnbonding,
    'delegationCapacity': delegationCapacity,
    'delegationCapacityPercentage': delegationCapacityPercentage,
    'rewardUnlockDate': rewardUnlockDate
}

# Bulk update database
db = TinyDB('./db.json', default_table='general')
db.purge_tables()
db.insert(general)
table = db.table('validators')
table.insert_multiple(stakerInfos)
