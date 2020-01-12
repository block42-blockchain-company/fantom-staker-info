pragma solidity ^0.5.0;

import "./Ownable.sol";

contract StakersInterface {
  function getStakerID(address addr) external view returns (uint256);
}

contract StakerInfo is Ownable {
  mapping (uint => string) public stakerInfos;

  address internal stakerContractAddress;

  constructor(address _stakerContractAddress) public {
    stakerContractAddress = _stakerContractAddress;
  }

  function updateStakerContractAddress(address _stakerContractAddress) external onlyOwner {
    stakerContractAddress = _stakerContractAddress;
  }

  event InfoUpdated(uint256 stakerID);

  function updateInfo(string calldata _configUrl) external {
    StakersInterface stakersInterface = StakersInterface(stakerContractAddress);

    // Get staker ID from staker contract
    uint256 stakerID = stakersInterface.getStakerID(msg.sender);

    // Check if address belongs to a staker
    require(stakerID != 0, "Address does not belong to a staker!");

    // Update config url
    stakerInfos[stakerID] = _configUrl;

    emit InfoUpdated(stakerID);
  }

  function getInfo(uint256 _stakerID) external view returns (string memory) {
    return stakerInfos[_stakerID];
  }
}