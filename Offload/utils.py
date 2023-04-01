#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 15:25
# @Author  : archer_oneee
# @File    : mySha256.py
# @Software: PyCharm
import hashlib
def my_sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    digest = my_sha256('a')
    print(digest)
    print(len(digest))