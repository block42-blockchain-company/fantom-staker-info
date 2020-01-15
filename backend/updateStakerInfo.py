import json
import urllib.request

from tinydb import TinyDB
from web3 import Web3

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

stakerInfos = []

bootstrapInfoMap = {
    13: {
        "name": "Fantom Vietnam",
        "website": "https://fantomviet.com",
        "contact": ""
    },
    15: {
        "name": "Fantom Validator",
        "website": "https://www.fantomvalidator.com",
        "contact": ""
    },
    16: {
        "name": "bu1137",
        "website": "https://keybase.io/nickai",
        "contact": ""
    },
    17: {
        "name": "GoFantom",
        "website": "https://gofantom.net",
        "contact": ""
    },
    18: {
        "name": "GoStake Network",
        "website": "https://gostake.com",
        "contact": ""
    },
    19: {
        "name": "Fantom Ukraine",
        "website": "",
        "contact": ""
    },
    20: {
        "name": "Binary Fintech Group",
        "website": "http://binaryfin.com",
        "contact": ""
    },
    21: {
        "name": "Fantom Global",
        "website": "https://fantom.global",
        "contact": ""
    },
    22: {
        "name": "Fantom Russian",
        "website": "",
        "contact": ""
    },
    24: {
        "name": "lopalcar",
        "website": "https://fantomstakers.com",
        "contact": ""
    },
    27: {
        "name": "Cryptoast.io",
        "website": "https://cryptoast.io",
        "contact": ""
    },
    28: {
        "name": "Hyperblocks",
        "website": "https://hyperblocks.pro",
        "contact": ""
    }
}

# Get infos for all validators
for stakerId in range(1, numValidators + 1):
    # Get the validator configUrl
    configUrl = stakerInfoContract.functions.stakerInfos(stakerId).call()

    name = ""
    website = ""
    contact = ""
    keybasePubKey = ""
    logoUrl = ""
    description = ""
    isVerified = configUrl is not ''

    # Get info from config url if available
    if configUrl is not '':
        response = json.loads(urllib.request.urlopen(configUrl).read().decode())

        for key, value in response.items():
            if key == 'name':
                name = value
            elif key == 'website':
                website = value
            elif key == 'contact':
                contact = value
            elif key == 'logoUrl':
                logoUrl = value
            elif key == 'description':
                description = value
    else:
        # No config in smart contract found, so use bootstrap values
        if stakerId in bootstrapInfoMap:
            name = bootstrapInfoMap[stakerId]['name']
            website = bootstrapInfoMap[stakerId]['website']
            contact = bootstrapInfoMap[stakerId]['contact']

    # Get the public variable stakers which includes some validator staking information
    sfcStakerInfo = sfcContract.functions.stakers(stakerId).call()

    # Calculate the total tokens staked to a validator = selfstaked + delegated
    selfStaked = sfcStakerInfo[5] / 1e18
    delegated = sfcStakerInfo[7] / 1e18
    totalstaked = selfStaked + delegated

    # Calculate the available delegation amount for the validator
    availableDelegationAmount = selfStaked * 15 - delegated

    # Calculate the available delegation amount
    availableDelegationPercent = availableDelegationAmount / (selfStaked * 15)

    # Get additional info from fantom.network api
    stakerApiUrl = "https://api.fantom.network/api/v1/staker/id/" + str(stakerId) + "?verbosity=2"
    response = json.loads(urllib.request.urlopen(stakerApiUrl).read().decode())
    apiStakerInfo = response['data']

    isCheater = False
    missedBlocks = 0
    delegatedMe = 0

    for key, value in apiStakerInfo.items():
        if key == 'isCheater':
            isCheater = value
        if key == 'missedBlocks':
            missedBlocks = int(value)
        if key == 'delegatedMe':
            delegatedMe = int(value) / 1e18

    # Calculate current withrawn Delegation Amount
    withdrawnDelegationAmount = delegatedMe - delegated

    # Get block height
    # txApiUrl = "https://api.fantom.network/api/v1/get-transactions"
    # response = json.loads(urllib.request.urlopen(txApiUrl).read().decode())
    # txApiInfo = response['data']
    # blockHeight = txApiInfo['maxBlockHeight']

    # Calculate productivity
    # productivity = ((int(blockHeight) - int(missedBlocks)) / int(blockHeight))

    stakerInfos += [{
        'id': stakerId,
        'name': name,
        'website': website,
        'contact': contact,
        'isVerified': isVerified,
        'logoUrl': logoUrl,
        'description': description,
        'address': sfcStakerInfo[8],
        'selfStaked': selfStaked,
        'totalStaked': totalstaked,
        'availableDelegationAmount': availableDelegationAmount,
        'isCheater': isCheater,
        'missedBlocks': missedBlocks,
        'withdrawnDelegationAmount': withdrawnDelegationAmount
    }]

# Bulk update database
db = TinyDB('./db.json')
db.purge()
db.insert_multiple(stakerInfos)
