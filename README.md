## Fantom Staker Info

<div>
  <a href="#">
    <img src="https://img.shields.io/badge/language-solidity-green.svg" alt="Language" />
  </a>
  <a href="https://explorer.fantom.network/address/0x92ffad75b8a942d149621a39502cdd8ad1dd57b4">
    <img src="https://img.shields.io/badge/network-fantom-3478ef.svg" alt="Fantom" />
  </a>
  <a href="https://fantomstaker.info">
    <img src="https://img.shields.io/badge/dapp-live-brightgreen.svg" alt="dApp" />
  </a>
  <a href="https://t.me/block42_fantom">
    <img src="https://img.shields.io/badge/contact-telegram-0088cc.svg" alt="Telegram" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
  </a>
</div>

<br />

A dApp on the Fantom Opera network to browse information about its validators.

## How does it work

We created a [smart contract](https://github.com/block42-blockchain-company/fantom-staker-info/blob/master/smart-contract/contracts/StakerInfo.sol) that interacts with the [SFC smart contract](https://github.com/Fantom-foundation/fantom-sfc/blob/master/contracts/sfc/Staker.sol). It allows each Fantom validator to add information (a URL to a `JSON` file) about themselves, so delegators have more insights who they are, without the involvement of a third party.

## Usage

The smart contract is already deployed and can be found on the Fantom Opera MainNet:

```solidity
0x92ffad75b8a942d149621a39502cdd8ad1dd57b4
```

### Config File

Create a config file in `JSON` format that contains the following parameters (you can also leave parameters empty):

```json
{
  "name": "VALIDATOR_NAME",
  "website": "WEBSITE_URL",
  "contact": "CONTACT_URL",
  "keybasePubKey": "KEYBASE_64_BIT_PUBLIC_KEY",
  "logoUrl": "LOGO_URL",
  "description": "DESCRIPTION_TEXT"
}

// This is how it could look like 👇

{
  "name": "block42",
  "website": "https://block42.tech",
  "contact": "https://t.me/block42_fantom",
  "keybasePubKey": "C57B29418AE33CC0",
  "logoUrl": "https://files.b42.tech/fantom/block42.png",
  "description": "We invest into the most promising crypto ecosystems and help them secure their networks. We provide consulting and development services on top of those protocols to bring adoption and use to them."
}
```

Then host it somewhere so it is publicly accessible!

### Update your validator info

1. Connect to your validator node
2. Open up a lachesis console session via `lachesis attach`
3. Load the StakerInfo contract ABI and instantiate the contract

```solidity
abi = JSON.parse('[{"inputs":[{"internalType":"address","name":"_stakerContractAddress","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"stakerID","type":"uint256"}],"name":"InfoUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"constant":true,"inputs":[],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakerInfos","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_stakerContractAddress","type":"address"}],"name":"updateStakerContractAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_configUrl","type":"string"}],"name":"updateInfo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"_stakerID","type":"uint256"}],"name":"getInfo","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
stakerInfoContract = web3.ftm.contract(abi).at("0x92ffad75b8a942d149621a39502cdd8ad1dd57b4")
```

4. Call the `updateInfo` function of the StakerInfo contract (make sure you have enough FTM on your wallet to cover the transaction fee)

```solidity
stakerInfoContract.updateInfo("CONFIG_URL", { from: "VALIDATOR_ADDRESS" })
// e.g.: stakerInfoContract.updateInfo("https://files.b42.tech/fantom/config.json", { from: "0xa4ddde0afdaea05a3d5a2ec6b5c7f3fc9945020b" })
```

5. Validate if you updated your info correctly

```solidity
stakerInfoContract.getInfo(VALIDATOR_ID)
// e.g.: stakerInfoContract.getInfo(14)
```

## Support

If you have any issues updating your validator info do not hesitate to join our [validator group](https://t.me/block42_fantom) or contact [me](https://t.me/christianlanz) directly.

## Licence

This project is licensed under the MIT license.

```
The MIT License

Copyright (c) 2020 block42 Blockchain Company GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
