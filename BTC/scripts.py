from bitcoinutils.script import Script
from BTC.identity import Id
from BTC import init
from BTC import consts
from BTC import scripts

init.initNetwork()

'''
def get_script_TXs(id_Alice: Id, id_Bob: Id, id_Ingrid: Id, timedelay: int) -> Script:
    return Script([
        id_Alice.pk.to_hex(), 'OP_CHECKSIGVERIFY',
        'OP_DUP', id_Bob.pk.to_hex(), 'OP_CHECKSIG',
        'OP_IF',
        'OP_DROP', id_Ingrid.pk.to_hex(), 'OP_CHECKSIG',
        'OP_ELSE',
        timedelay, 'OP_CHECKSEQUENCEVERIFY',
        'OP_ENDIF'])

    先验证A的签名,如果有B的签名,那么再加上I的签名可以使用该输出。如果没有B的签名那么A可以在时间锁之后直接使用该输出
'''

def get_script_TXs(id_Alice: Id, id_Ingrid: Id) -> Script:
    return Script([
        id_Alice.pk.to_hex(), 'OP_CHECKSIGVERIFY', id_Ingrid.pk.to_hex(), 'OP_CHECKSIGVERIFY', 0x1])
    # 先验证Alice的签名再验证Ingrid的签名，都正确之后可使用该输出。


def get_script_txa_v(id_a: Id, id_i: id, timedelay: int) -> Script:
    return Script([
        id_i.pk.to_hex(), 'OP_CHECKSIGVERIFY',
        'OP_DUP', id_a.pk.to_hex(), 'OP_CHECKSIG',
        'OP_NOTIF',
        timedelay, 'OP_CHECKLOCKTIMEVERIFY',
        'OP_ENDIF'])


def getScriptTXf(idA: Id, idB: Id):
    scriptFToutput = Script([
        idA.pk.to_hex(), 'OP_CHECKSIGVERIFY', idB.pk.to_hex(), 'OP_CHECKSIGVERIFY', 0x1])  # input: sigB, sigA
    return scriptFToutput


def get_script_3sig(id_a: Id, id_b: Id, id_i: Id) -> Script:
    script = Script([
        id_a.pk.to_hex(), 'OP_CHECKSIGVERIFY', id_b.pk.to_hex(), 'OP_CHECKSIGVERIFY', id_i.pk.to_hex(),
        'OP_CHECKSIGVERIFY', 0x1])  # input: sigB, sigA
    return script


def get_script_2sig(id_1: Id, id_2: Id) -> Script:
    # id_a.pk.to_hex()：以十六进制字符串形式返回 public key（SEC格式-默认压缩）
    script = Script([
        id_1.pk.to_hex(), 'OP_CHECKSIGVERIFY', id_2.pk.to_hex(), 'OP_CHECKSIGVERIFY', 0x1])  
    return script


def get_script_ct(id_a: Id, id_b: Id, id_i: Id, id_punish_vc: Id, id_punish_channel: Id, rev_hash, timedelay1: int,
                     timedelay2: int) -> Script:
    return Script([
        'OP_NOTIF',
        0x3, id_a.pk.to_hex(), id_i.pk.to_hex(),id_b.pk.to_hex(), 0x3, 'OP_CHECKMULTISIGVERIFY', timedelay1,
        'OP_CHECKSEQUENCEVERIFY',
        'OP_ELSE',
        'OP_1SUB',
        'OP_NOTIF',
        id_punish_channel.pk.to_hex(), 'OP_CHECKSIGVERIFY', 'OP_HASH256', rev_hash, 'OP_EQUALVERIFY',
        'OP_ENDIF', 0x1])

def get_script_ln_ct(id_a: Id, id_b: Id, id_i: Id, id_punish_vc: Id, id_punish_channel: Id, rev_hash, timedelay1: int,
                     timedelay2: int) -> Script:
    """
    spend with either: 
    sig_a, sig_i, sig_b, 0 (after timedelay1) -> 需要三个人的签名该TXc才能被取用
    or
    rev_secret sig_punish_channel 1 -> 闪电通道的惩罚
    """
    return Script([
        'OP_NOTIF',
        0x3, id_a.pk.to_hex(), id_i.pk.to_hex(),id_b.pk.to_hex(), 0x3, 'OP_CHECKMULTISIGVERIFY', timedelay1,
        'OP_CHECKSEQUENCEVERIFY',
        'OP_ELSE',
        'OP_1SUB',
        'OP_NOTIF',
        id_punish_channel.pk.to_hex(), 'OP_CHECKSIGVERIFY', 'OP_HASH256', rev_hash, 'OP_EQUALVERIFY',
        'OP_ENDIF', 0x1])   


# 闪电网络 commitment transaction
def get_output_ln_ct(id_post: Id, id_punish: Id, rev_hash, timedelay: int) -> Script:
    """
    spend with either: 
    sig_post, 0 (after timedelay)
    or
    rev_secret sig_punish, 1 (after timedelay1)
    """
    return Script([
        'OP_NOTIF',
        id_post.pk.to_hex(), 'OP_CHECKSIGVERIFY', timedelay, 'OP_CHECKSEQUENCEVERIFY',
        'OP_ELSE',
        id_punish.pk.to_hex(), 'OP_CHECKSIGVERIFY', 'OP_HASH256', rev_hash, 'OP_EQUALVERIFY',
        'OP_ENDIF', 0x1])


# 闪电网络下有时效性虚拟通道的commitment transaction脚本
def get_script_ln_ct_val(id_l: Id, id_r: Id, id_punish_vc: id, id_punish_channel: id, rev_hash, timedelay1: int,
                         timedelay2: int) -> Script:
    """
    spend with either:
    sig_l, sig_r, 0 (after timedelay1)
    or
    rev_secret sig_punish_channel 1
    or
    sig_punish_vc, 2 (after timedelay2)
    """
    return Script([
        'OP_NOTIF',
        0x2, id_l.pk.to_hex(), id_r.pk.to_hex(), 0x2, 'OP_CHECKMULTISIGVERIFY', timedelay1, 'OP_CHECKSEQUENCEVERIFY',
        'OP_ELSE',
        'OP_1SUB',
        'OP_NOTIF',
        id_punish_channel.pk.to_hex(), 'OP_CHECKSIGVERIFY', 'OP_HASH256', rev_hash, 'OP_EQUALVERIFY',
        'OP_ELSE',
        id_punish_vc.pk.to_hex(), 'OP_CHECKSIGVERIFY', timedelay2, 'OP_CHECKLOCKTIMEVERIFY',
        'OP_ENDIF',
        'OP_ENDIF', 0x1])
