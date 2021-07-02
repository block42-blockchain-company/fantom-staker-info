const StakersContract = artifacts.require("./contracts/Stakers.sol");
const StakerInfoContract = artifacts.require("./contracts/StakerInfo.sol");

module.exports = function(deployer) {
  deployer.deploy(StakersContract).then(() => {
    return deployer.deploy(StakerInfoContract, StakersContract.address);
  });
};