pragma solidity ^0.5.0;

import "./Ownable.sol";

contract StakersInterface {
  function getStakerID(address addr) external view returns (uint256);
}

contract StakerInfo is Ownable {
  mapping (uint => string) stakerInfos;

  address stakerContractAddress;

  constructor(address _stakerContractAddress) public {
    stakerContractAddress = _stakerContractAddress;
  }

  function updateStakerContractAddress(address _stakerContractAddress) public onlyOwner {
    stakerContractAddress = _stakerContractAddress;
  }

  event Updated(uint256 stakerID);

  function update(string memory _configUrl) public {
    StakersInterface stakersInterface = StakersInterface(stakerContractAddress);

    // Get staker ID from staker contract
    uint256 stakerID = stakersInterface.getStakerID(msg.sender);

    // Check if address belongs to a staker
    require(stakerID != 0, "Address does not belong to a staker!");

    // Update config url
    stakerInfos[stakerID] = _configUrl;

    emit Updated(stakerID);
  }

  function stakerInfo(uint256 _stakerID) external view returns (string memory) {
    return stakerInfos[_stakerID];
  }
}