#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 08:20
# @Author  : archer_oneee
# @File    : Node.py
# @Software: PyCharm
import random

from eth_account import Account
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.auto import w3


class Node:
    sk = None
    account = None
    addr = None

    def __init__(self, sk):
        self.sk = sk
        self.account: LocalAccount = Account.from_key(sk)
        self.addr = self.account.address

    def to_32byte_hex(self, val):
        return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))


    def sign_message(self, msg):
        message = encode_defunct(text=msg)
        signed_message = w3.eth.account.sign_message(message, self.sk)
        ec_recover_args = (msghash, v, r, s) = (
            Web3.to_hex(signed_message.messageHash),
            signed_message.v,
            self.to_32byte_hex(signed_message.r),
            self.to_32byte_hex(signed_message.s),
        )
        return ec_recover_args, signed_message

    def sig_verify(self, msg, sig):
        message = encode_defunct(text=msg)
        result = w3.eth.account.recover_message(message, signature=sig.signature)
        print(result)
        if result == self.addr:
            return True
        else:
            return False

    def get_randomsk(self):
        p = 'FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141'.replace(' ', '')
        for i in range(0,10):
            num = random.randint(0,int(p,16))
            print(hex(num))

if __name__ == '__main__':
    sk = '0xe62248374af86aa480f9cebd44f04cd02b915130d4fbda885a201488257b0a17'

    msg = "abcd"
    node = Node(sk)
    # node.get_randomsk()

    ec_recover,sig = node.sign_message(msg)
    ec_result = node.sig_verify(msg,sig)
    print(ec_recover)