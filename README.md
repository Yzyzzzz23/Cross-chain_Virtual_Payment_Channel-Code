## Cross-chain_Virtual_Payment_Channel-Code

### Abstract

With the emergence of countless independent blockchain systems in recent years, cross-chain transactions have attracted considerable attention, and lots of solutions have been put forth by both industry and academia. However, most of existing solutions suffer from either centralization or scalability issues. To mitigate these issues, in this paper, we propose the concept of cross-chain virtual payment channels, which allows two users in different blockchain systems to conduct limitless off-chain transactions with the help of an intermediate node, hence solving the centralization and scalability issues. Furthermore, as the intermediate node is only involved in the channel open and close operations, it further improves the efficiency of cross-chain transactions, and to a certain extent, it even enhances the privacy of the cross-chain transaction. Meanwhile, we also present the first concrete cross-chain virtual payment channel scheme, which only requires one of the blockchain systems supporting the Turing-complete scripting language. The corresponding detailed security analysis in the Universal Composability framework demonstrates that our proposal holds the Consensus on Open, Update, and Close. Finally, we implement and deploy our cross-chain virtual payment channel scheme on the Ethereum and Bitcoin test networks. The extensive experimental results show that our proposal dramatically improves the efficiency of cross-chain transactions, and the advantage becomes more pronounced as the number of transactions increases.

### Introduction

A simple demo to create and evaluate the required transactions for cross-virtual payment channel on Bitcoin and Ethereum.

### Usage

- Install Python >= 3.7.3
- Install dependencies (check requirements.txt)

### Directory Description

- BTC: In this directory, we implement the generalized channel and the corresponding cross-chain virtual channel on Bitcoin. The reader can run the main.py to construct the required transactions.

- ETH: In this directory, we implement the payment channel on Ethereum using the smart contract. To run this code, the reader needs to install [Ganache](https://trufflesuite.com/ganache/) as the underlying blockchain platform. The files with the suffix ".sol" are the required smart contract, and the files with the suffix ".abi" or ".bin" are the corresponding compiled result.

- OffLoad: In this directory, we implement a sidechain as an "oracle" to send the state of Bitcoin to the smart contract on Ethereum. The reader can try to run "main.py" to start the sidechain.
