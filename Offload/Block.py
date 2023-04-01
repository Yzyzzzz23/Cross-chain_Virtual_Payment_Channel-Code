#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 15:13
# @Author  : archer_oneee
# @File    : Block.py
# @Software: PyCharm
import BlockHead
import SignVerfiy
import utils


class Block:

    prevHash = utils.my_sha256('0')
    height = 0
    blockHash = utils.my_sha256('0')
    head = None
    body = []
    size = 0
    commiteeAddr = ['0x2eCcc99c951538F3acc0a470c1833c430DC4C63F',
                    '0x6Be3ebEe0e105C1c404599bd52a6a714dB767eB5',
                    '0x1AbB05903dA93668B031b55Cc21146F0bBb7154d',
                    '0xb88b29d5C82D9b9067e443934A19aDd2859602fA',
                    '0x31772F29C6274F4b120FBc3534A15B0adD220E06']

    def mine(self, preBlock, info, memSigs):
        count = 0
        agreeAddr = []
        for memSig in memSigs:
            addr = SignVerfiy.sig_verify(info, memSig)
            agreeAddr.append(addr)
        agreeAddr = list(set(agreeAddr))
        headL = []
        for addr in agreeAddr:
            if addr in self.commiteeAddr:
                headL.append(addr)
        if len(headL) < 3:
            return False
        self.body.append(info)
        self.height += preBlock.height + 1
        self.prevHash = preBlock.blockHash
        self.head = BlockHead.block_head(self.size + 225, headL)
        self.getBlkHash()
        return True

    def getSize(self):
        count = 0
        count += len(self.prevHash)
        count += len(str(self.height))
        count += 64
        count += len(''.join(self.body))
        self.size = count

    def getBlkHash(self):
        string = ''

        string += self.prevHash
        string += str(self.height).ljust(8,'0')
        string += str(self.size).ljust(8,'0')
        string += ''.join(self.body)
        self.blockHash = utils.my_sha256(string)



