# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import Mine
import utils
from Block import Block
from Node import Node

BitcoinTx = 'd45d1465e58f51a4794c8a76a92a6ea8145e9b276e5b70f43b09740ca4d766e9'

AliceSk = '0x757b58f982c50e8a3972f21ab920e5c40bd8fa148b2398fa9cf556e25a3a7c0a'
BobSk = '0x8c4f94ebb1b073f719e42877a72d2338c045c3f22afbc242c443943e09041b40'
IngridSk = '0x8c547b68c7f93276888153ea63d76e91d4511c90d9355055249b80d7036caadc'

skList = ['0x1a35edca020d3ffc2ecb17c0ecf05ee22eef021b3521f23c5d48b198a423b773',
      '0xce84a2257003f24ab610a6dd1b038a2e03dc2968d9261a7def647ef7aca5fc79',
      '0xdce2e0ea2808cd3ea1b2d6762ef61e9c1b07820de17f48aaea5b150a268f99cf',
      '0x98fc7b9b5d5ecbdebfc46738227cca5747d97e0fc6ac9e41a992dc9a3089bb3f',
      '0xfcfbc3acd036ee9cbb6d5aa4a19611521c6b9410445629f57654f152bf4e1ce5']

nodeList = []
for sk in skList:
      node = Node(sk)
      nodeList.append(node)

genesis_block = Block()
blockList = [genesis_block]

while True:
      Mine.mine(blockList, nodeList, BitcoinTx)
