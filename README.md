# Udemy blockchain learning
course link: https://www.udemy.com/share/101WhE3@mlTBlul6ifabSA1152N_ogX5N_mkqxp3n7fHmzjbvzZHbr2eQONtyfJllGbC35wTdw==/

## content
### section 1 (theoretical)
Blockchain
- block 1
    - Hash: signature of current block
    - Immutable Ledger: can not be modified, or too hard to be modified
    - Distributed Network: the key point of decentralized characteristic
        - Byzantine Problem
    - Mining: the process to create a block which can link to blockchain
    - Consensus Protocol ()
        - PoW (Proof of Work)
        - PoS (Proof of Stake)
- block 2
- ...
- block n

### module 1 (coding)
Description: 
create a simple blockchain which support mining, getting whole chain and so on.

Key tech:
- Flask
- HTTP
- JSON
- Hash (SHA256)
- Basic concept introduced in section 1


### section 2 - Plan of Attack (Miner prospect)
#### Bitcoin
Bitcoin monetary policy
- The Halving
    - Every 4 years, the reward of mining decreased twice
- Block frequency
    - How often a block is created
#### Mining difficulty
- Current Target
- Max Target
- Mining difficulty
    - Control leading zero to adjust difficulty
    - Difficulty is adjusted every 2016 blocks
    - Difficulty = current target / max target
#### Mining pools
- to allocate task to ensure that different miners do not calculate same hash
- allocate reward by power contributed
#### Nonce range
- one nonce range: 32-bit unsigned number
- Conclusion: Only Nonce is not enough
- A block contains timestamp!
- Problem: Hash rate is too high, timestamp is not enough either
#### How miners pick transactions
- Transactions come from mempools
- Transactions contain fees, which is not compulsory
- strategy of picking transactions can continuing change with Mining pools or big machine which has over qualified hash rate
    1. pick high fee transactions
    2. pick second high transactions
#### CPUs vs GPUs vs ASICs
- CPU: central processing unit
    - < 10 MH/s
- GPU: graphics processing unit
    - < 1 GH/s
- ASIC: application-specific integrated circuit
    - do SHA256 on physical level
        - \> 1000 GH/s
- Cloud Mining
- Different cryptocurrencies have different mining policy. So ASICs is not general.
    - Bitcoin use SHA256
    - Ethereum use its own hash policy, which is related to memory
#### Mempools
- there is a mempool with each miner
#### Orphaned blocks
- Wait couple of new blocks to confirm transactions
#### 51% attack*
- get 51% or more hashrate
- double spends problem
- When a group of hidden participants with majority computational power conduct mining without announcing their version of the chain to the rest of the network. The attackers can benefit by leveraging the double-spend problem.
#### Bits to Target conversion
1. Bits(Dec) -> Hex: 392009692 -> 175D97DC
2. Hex[0:2] -> Dec: 17 -> 23 (the number of bytes of current target)(23 bytes -> 46 hex digits)
3. current_target[0:len(Hex[2:])] = Hex[2:]: 5D97DC000000......00000 (total 46 hex digits)
4. complement current_target to 64 hex digits: 000...5D97DC0000..00 (total 64 hex digits)
Target is stored in every block, but it's in "Bits" (a decimal) format.


### module 2 (coding)
key part: decentralize blockchain (consensus protocal) and create transactions (make blockchain become cryptocurrency)


we can regard cryptocurrency as the combination of blockchain and transactions, where blockchain play a role as infrastructure and transactions play a role as data store in blockchain.