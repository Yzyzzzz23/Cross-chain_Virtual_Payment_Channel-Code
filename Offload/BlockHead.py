#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 15:28
# @Author  : archer_oneee
# @File    : BlockHeader.py
# @Software: PyCharm
class block_head:
    size = 0  #8
    agreeNum = 0 #8
    agreeMember = [] # 42 * 5

    def __init__(self, size=0, agreeMember=[]):
        self.size = size
        self.agreeMember = agreeMember
        self.agreeNum = len(agreeMember)


    def getString(self):
        return str(self.size).ljust(8,'0') + str(self.agreeNum).ljust(8,'0') + ''.join(self.agreeNum)

    def getSize(self):
        return (8 + 8 + 42 * 5)