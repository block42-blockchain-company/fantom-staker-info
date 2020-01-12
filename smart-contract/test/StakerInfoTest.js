const assert = require("assert");
const ganache = require("ganache-cli");
const Web3 = require("web3");
const web3 = new Web3(ganache.provider());

const StakersContract = artifacts.require("./contracts/Stakers.sol");
const StakerInfoContract = artifacts.require("./contracts/StakerInfo.sol");

contract('StakerInfo', async () => {
  it("should fail to create a staker", async () => {
    const contract = await StakersContract.deployed();

    let success = true;
    try {
      await contract.createStake(web3.utils.toHex(""), { value: web3.utils.toWei("0.5") });
    } catch (error) {
      success = false;
    }

    assert(success == false);
  })

  it("should successfully create a staker", async () => {
    const contract = await StakersContract.deployed();
    await contract.createStake(web3.utils.toHex(""), { value: web3.utils.toWei("1") });
    const stakersNum = await contract.stakersNum();
    assert(stakersNum == 1);
  })

  it("should update staker info", async () => {
    const contract = await StakerInfoContract.deployed();
    await contract.updateInfo("https://fantom.b42.tech/config.json");
    const configUrl = await contract.getInfo(1);
    assert(configUrl == "https://fantom.b42.tech/config.json");
  })
})