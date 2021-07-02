const SfcAbiProxy = artifacts.require("./contracts/SfcAbiProxy.sol");

module.exports = function(deployer) {
  deployer.deploy(SfcAbiProxy, "0xfc00face00000000000000000000000000000000");
};