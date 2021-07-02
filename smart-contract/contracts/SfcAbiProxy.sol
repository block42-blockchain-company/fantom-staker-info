pragma solidity ^0.5.0;

contract SfcInterface {
  mapping(address => uint256) public getValidatorID;
}

contract SfcAbiProxy {
  address internal sfcAddress;

  constructor(address _sfcAddress) public {
    sfcAddress = _sfcAddress;
  }

  function getStakerID(address addr) external view returns (uint256) {
    SfcInterface sfc = SfcInterface(sfcAddress);

    // Proxy the getStakerID call to the SFC using it's new ABI
    uint256 validatorId = sfc.getValidatorID(addr);

    return validatorId;
  }
}