from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence, TYPE_RELATIVE_TIMELOCK, \
    TYPE_ABSOLUTE_TIMELOCK
from identity import Id
import txs
from helper import hash256, print_tx, gen_secret
from bitcoinutils.setup import setup
from bitcoinutils.proxy import NodeProxy
import json


# 比特币一方构建交易
def main():

    # 随机生成交易地址
    id_Alice = Id('e12046ad146a0f15bcf977c86181828f1e0472ea1bd2efe9af6362c8d533ac11')      #addr moUDVi9sE5J14w7a9tAMeY4zanp2ghzgXB
    id_Ingrid = Id('e12046ad146a0f15bcf977c86181828f1e0472ea1bd2efe9af6362c8d5312345')     #addr mnUmE2gf8z3qrXaQZ93rB6VP3h4sLaT9XS
    id_Bob = Id('e12046ad146a0f15bcf977c86181828f1e0472ea1bd2efe9af6362eed53a41a7')        #addr mvQpYtrYEjG4zLuXZPDV9VprJCi1SkrWdD


    tx_in_Alice = TxInput('f14fb1b38127f18dcb0d7dbf6745fb0cc28baf8de0b37373d3e1f131383ead47', 1)
    tx_in_Ingrid = TxInput('bacf8061fa33a2149d6320bb4a6900249bb23434f4cc4f68c1f8e699a3f90ba8', 0)

    c = 9000 # 交易金额
    fee = 300 # 上链费用

    # funding transaction
    TXc_Alice_Ingrid_L = txs.get_TX_multisig(tx_in_Alice, tx_in_Ingrid, id_Alice, id_Ingrid, c - fee, fee)
    print_tx(TXc_Alice_Ingrid_L,'** TXc_Alice_Ingrid_L **')
    # print_tx('e19d78f91a2c65ff01cac0bbd14dc7c6431e310a5903e6bf88f10ecc5c728b10')
    # 交易ID： e19d78f91a2c65ff01cac0bbd14dc7c6431e310a5903e6bf88f10ecc5c728b10
    # 交易脚本：020000000247ad3e3831f1e1d37373b3e08daf8bc20cfb4567bf7d0dcb8df12781b3b14ff1010000006b483045022100d29417883b7acebdd
    # 11aa343f89acb84dc4970ec4423c2715a37d6881a942bb30220011b43659b8cae215cb3f59e480f20ffaf7d947cb36ae2bf218239d17a36998f0121034
    # 224f6eb190525af63546d2f1cabbb7b182bb26f5911f5eeeddbd18edd78b78bffffffffa80bf9a399e6f8c1684fccf43434b29b2400694abb20639d14a
    # 233fa6180cfba000000006a4730440220497c28ece6c25640c26c66a246b474870c29f334c5ebd1f30ac536937c8ef60a0220221045d930e8b512c67e8
    # c66188ce2b81a08583e217a50c88a687c308d96be0d012103b84f704cf460e14dd30acf27868de6b31485cf50154a6cc6c2c3e6f823a3aeffffffffff0
    # 1e4250000000000004721034224f6eb190525af63546d2f1cabbb7b182bb26f5911f5eeeddbd18edd78b78bad2103b84f704cf460e14dd30acf27868de
    # 6b31485cf50154a6cc6c2c3e6f823a3aeffad5100000000

    # split transaction
    TXs_Alice_Ingrid = txs.get_TXs(TxInput(TXc_Alice_Ingrid_L.get_txid(), 0), id_Alice, id_Ingrid, c - 2*fee, fee)
    print_tx(TXs_Alice_Ingrid,'** TXs_Alice_Ingrid **')
    # 交易ID：d45d1465e58f51a4794c8a76a92a6ea8145e9b276e5b70f43b09740ca4d766e9
    # 交易脚本：0200000001108b725ccc0ef188bfe603590a311e43c6c74dd1bbc0ca01ff652c1af9789de10000000091483045022100f9add8e0a8642b648
    # 7d0ccd78b2fe71cc785d217bcf0d351f2e7ae40fe52b99e02204aecf717da45fd28824db4123aa502d50d8ec14ca9dccac0bdccf5a3ff0955d70147304
    # 4022031a200fcffd7b4410f18f90c68a2c9950c860850e4ddaeada64ab4224936ceb502207a61bc2c97a93193f3985b56947704ffc75808faf0cc33c88
    # c488829e9a67dc001ffffffff01b8240000000000004721034224f6eb190525af63546d2f1cabbb7b182bb26f5911f5eeeddbd18edd78b78bad2103b84
    # f704cf460e14dd30acf27868de6b31485cf50154a6cc6c2c3e6f823a3aeffad5100000000

    # The transaction TX_f:
    TXf_Alice_Bob_V = txs.get_TXf_V(TxInput(TXs_Alice_Ingrid.get_txid(), 0), id_Alice, id_Ingrid, id_Bob, c - 3*fee, fee)
    print_tx(TXf_Alice_Bob_V, '** TXf_Alice_Bob_V **:')
    # 交易ID：  
    # 交易脚本：0200000001e966d7a40c74093bf4705b6e279b5e14a86e2aa9768a4c79a4518fe565145dd40000000092483045022100a57bc3be1b5afabf0
    # fcde51096b389ca0670899090c386e965d305e52f1a567c02201adddd39154f39d91d27762ce2258bb5259ae685c3011b2629a1aa40602c7e160148304
    # 5022100a4184b35fb02abef7551a6825b13bc089630860a356624decd455b043b4b0836022013ef4a2a888b49ae64306aa6401c6559164f60b4d9e18ff
    # 110f8e6066064e71d01ffffffff0128230000000000004721034224f6eb190525af63546d2f1cabbb7b182bb26f5911f5eeeddbd18edd78b78bad21032
    # c2f9e859ece82753ce26fa443d397b75d0aa93d6ac896cf775ba3e95e670079ad5100000000
    


if __name__ == "__main__":
    main()

