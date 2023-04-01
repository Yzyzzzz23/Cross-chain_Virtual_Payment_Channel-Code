#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 19:15
# @Author  : archer_oneee
# @File    : signTest.py
# @Software: PyCharm
from web3 import Web3, EthereumTesterProvider
from eth_account.messages import encode_defunct
w3 = Web3(EthereumTesterProvider())
msg = "abcd"
private_key = 'e62248374af86aa480f9cebd44f04cd02b915130d4fbda885a201488257b0a17'
message = encode_defunct(text=msg)
signed_message = w3.eth.account.sign_message(message, private_key)

print(signed_message)

message = encode_defunct(text="abcd")
result = w3.eth.account.recover_message(message, signature=signed_message.signature)
print(result)