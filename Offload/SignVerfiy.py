#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 15:34
# @Author  : archer_oneee
# @File    : SignVerfiy.py
# @Software: PyCharm
from eth_account.messages import encode_defunct
from web3.auto import w3


def sig_verify(msg, sig):
    message = encode_defunct(text=msg)
    addr = w3.eth.account.recover_message(message, signature=sig.signature)
    return addr