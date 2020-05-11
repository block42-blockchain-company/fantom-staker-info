from modules.Database import Database

database = Database()

epochRewards = database.getAllRewards()
delegations = database.getAllDelegations()

stats = []

for reward in epochRewards:
    epoch = reward['_id']
    staked = list(filter(lambda delegation: delegation['startEpoch'] == epoch, delegations))
    unstaked = list(filter(lambda delegation: delegation['endEpoch'] == epoch, delegations))

    stats += [{
        'epoch': epoch,
        'staked': sum(delegation['amount'] for delegation in staked),
        'unstaked': sum(delegation['amount'] for delegation in unstaked),
        'rewardsBurned': reward['burnedReward']
    }]

print('Epoch,Staked,Unstaked,Rewards Burned')

for stat in stats:
    print(str(stat['epoch']) + ',' + str(stat['staked']) + ',' + str(stat['unstaked']) + ',' + str(stat['rewardsBurned']))
