#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 20:17
# @Author  : archer_oneee
# @File    : Mine.py
# @Software: PyCharm
from Block import Block


def mine(blkList, NodeList, txHash):
    preBlk = blkList[len(blkList)-1]
    sigs = []
    for node in NodeList:
        ec_recover_args, signed_message = node.sign_message(txHash)
        sigs.append(signed_message)
    newBlk = Block()
    result = newBlk.mine(preBlk,txHash, sigs)
    if result is True:
        print("block: " + str(newBlk.height) + " packs successfully!")
        blkList.append(newBlk)
    else:
        print("block: " + str(newBlk.height) + " packs unsuccessfully!")
