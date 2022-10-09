from base64 import decode
from inspect import signature
from xml.dom.minidom import TypeInfo
from eth_typing.encoding import HexStr
from sympy import sign
from toolz.itertoolz import count
from web3 import Web3
import json
import eth_keys
from eth_utils import decode_hex
from getpass import getpass
from web3.contract import transact_with_contract_function
from eth_account.messages import encode_defunct
import requests 
import time
import numpy as np

# 获取公钥
def getPublicKey(val):
  msg='abc'
  message=encode_defunct(text=msg)
  sign_message=web3.eth.account.sign_message(message,private_key=val)
  k=web3.eth.account.recover_message(message,signature=sign_message.signature)
  return k
def to_32byte_hex(val):
        return web3.toHex(web3.toBytes(val).rjust(32,b'\0'))

# 连接.sol文件，文件路径记得修改。
with open('/Users/yzyzzzz/Dropbox/Papers-Yuzhe/Cross-chain Virtual Channel_YZ/Cross-chain_virtual_payment_channel-Code/ETH/helloworld_sol_Greeter.abi', 'r') as f:
    abi = json.load(f)
with open('/Users/yzyzzzz/Dropbox/Papers-Yuzhe/Cross-chain Virtual Channel_YZ/Cross-chain_virtual_payment_channel-Code/ETH/helloworld_sol_Greeter.bin', 'r') as f:
    code = f.read()

with open('/Users/yzyzzzz/Dropbox/Papers-Yuzhe/Cross-chain Virtual Channel_YZ/Cross-chain_virtual_payment_channel-Code/ETH/committee1_sol_committee.abi', 'r') as f:
    abi_2 = json.load(f)
with open('/Users/yzyzzzz/Dropbox/Papers-Yuzhe/Cross-chain Virtual Channel_YZ/Cross-chain_virtual_payment_channel-Code/ETH/committee1_sol_committee.bin', 'r') as f:
    code_2 = f.read()


# 连接Ganache构建的以太坊私链
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
# print(web3 .isConnected())
if web3 .isConnected() == True:
  print("successful connection")

# 获取一下 Ingrid 和 Bob 的公钥
Ingrid = web3.eth.accounts[5]
Ingrid_privateKey = eth_keys.keys.PrivateKey(decode_hex('ac9124d290c659500d4e6beb043aa8674a6a8757f6b6034f32f3b15d21da8ace'))
Ingrid_publicKey = getPublicKey(Ingrid_privateKey)
print('Ingrid_publicKey:',Ingrid_publicKey)
Bob = web3.eth.accounts[6]
Bob_privateKey = eth_keys.keys.PrivateKey(decode_hex('db8048b9033ad279f02c3e84bd221ee210af84e27629f47279b0aaf5ea273f53'))
Bob_publicKey = getPublicKey(Bob_privateKey)
print('Bob_publicKey:',Bob_publicKey)



# 部署用于构建虚拟支付通道的智能合约
def Deployment_channel_contract():
  global Channels
  Greeter = web3.eth.contract(bytecode=code,abi=abi)
  option = {"from": Ingrid, "gas": 3000000}
  tx_hash = Greeter.constructor().transact(option)
  tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
  contract_address = web3.toChecksumAddress(tx_receipt.contractAddress)
  print("channel_contract_address:", contract_address)
  # 之后用Channels来调用智能合约的函数
  Channels = web3.eth.contract(contract_address,abi=abi)

# 投票委员会成员的账户：
Voter_1 = web3.eth.accounts[7]
Voter_2 = web3.eth.accounts[8]
Voter_3 = web3.eth.accounts[9]
# 部署委员会智能合约 
def Deployment_committee_contract():
  committee = web3.eth.contract(bytecode=code_2, abi=abi_2)
  option_2 = {"from": Voter_1, "gas": 3000000}
  tx_hash_2 = committee.constructor().transact(option_2)
  tx_receipt_2 = web3.eth.wait_for_transaction_receipt(tx_hash_2)
  committee_contract_address = web3.toChecksumAddress(tx_receipt_2.contractAddress)
  return committee_contract_address

# 用于保存Ingrig和Bob链下信息的数组（支付通道）
count=0
message=[] 
message_Ingrid=[]
sign_message_Ingrid=[]
ec_Ingrid_hash=[]
ec_Ingrid_v=[]
ec_Ingrid_r=[]
ec_Ingrid_s=[]
message_Bob=[]
sign_message_Bob=[]
ec_Bob_hash=[]
ec_Bob_v=[]
ec_Bob_r=[]
ec_Bob_s=[]
total_amount=0#总的转账钱数
total_amount_all=[]#每次的转账钱数


# 部署用于创建支付通道的合约（包含构建跨链虚拟通道的功能）
def deploy_lc(Ingrid,Bob,value):
  # 双方转钱给智能合约，value为金额
  tx_hash = Channels.functions.pay().transact({"from":Ingrid,"value":value})
  tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
  tx_hash2 = Channels.functions.pay().transact({"from":Bob,"value":value})
  tx_receipt2 = web3.eth.wait_for_transaction_receipt(tx_hash2)
  # 保存公钥
  tx_hash3 = Channels.functions.saveAccount_publickey(Ingrid_publicKey,Bob_publicKey).transact({"from":Ingrid,"value":value})
  tx_receipt3 = web3.eth.wait_for_transaction_receipt(tx_hash3)
  # 保存地址
  tx_hash4 = Channels.functions.saveAccount(Ingrid,Bob).transact({"from":Ingrid,"value":value})
  tx_receipt4 = web3.eth.wait_for_transaction_receipt(tx_hash4) 
  # 计算costs
  costs = tx_receipt.gasUsed + tx_receipt2.gasUsed
  # print( "部署支付通道合约的消耗: ",costs)

# 更新支付通道，更新Ingrid和Bob之间的消息
def update_lc(value=0):
  global count
  count = count + 1
  message.append('Number:count'+str(count)+'Ingrid.balance:'+ str(~value)+'Bob.balance:'+str(value))
  message_Ingrid.append(encode_defunct(text=message[count-1]))
  sign_message_Ingrid.append(web3.eth.account.sign_message(message_Ingrid[count-1], private_key = Ingrid_privateKey))
  # 对签名后的消息进行分割便于验证
  ec_recover_args_a = (msghash,v,r,s)=(web3.toHex(sign_message_Ingrid[count-1].messageHash),sign_message_Ingrid[count-1].v,
            to_32byte_hex(sign_message_Ingrid[count-1].r),to_32byte_hex(sign_message_Ingrid[count-1].s))
  ec_Ingrid_hash.append(ec_recover_args_a[0])
  ec_Ingrid_v.append(ec_recover_args_a[1])
  ec_Ingrid_r.append(ec_recover_args_a[2])
  ec_Ingrid_s.append(ec_recover_args_a[3])
  message_Bob.append(encode_defunct(text=message[count-1]))
  sign_message_Bob.append(web3.eth.account.sign_message(message_Bob[count-1],private_key=Bob_privateKey))
  # 对签名后的消息进行分割便于验证
  ec_recover_args_b=(msghash,v,r,s)=(web3.toHex(sign_message_Bob[count-1].messageHash),sign_message_Bob[count-1].v,
            to_32byte_hex(sign_message_Bob[count-1].r),to_32byte_hex(sign_message_Bob[count-1].s))
  ec_Bob_hash.append(ec_recover_args_b[0])
  ec_Bob_v.append(ec_recover_args_b[1])
  ec_Bob_r.append(ec_recover_args_b[2])
  ec_Bob_s.append(ec_recover_args_b[3])

# 关闭支付通道（乐观情况），即根据最新的支付通道状态分配智能合约里的资金
def close_lc(value):
  load_count_a = 1
  tx_hash = Channels.functions.submit_transaction_a(load_count_a,value,value,ec_Bob_hash[load_count_a-1],ec_Bob_v[load_count_a-1],
            ec_Bob_r[load_count_a-1],ec_Bob_s[load_count_a-1], 30).transact({"from":Ingrid,"value":0})
  tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
  load_count_b=1
  tx_hash2 = Channels.functions.submit_transaction_b(load_count_b,value,value,ec_Ingrid_hash[load_count_b-1],ec_Ingrid_v[load_count_b-1],
            ec_Ingrid_r[load_count_b-1],ec_Ingrid_s[load_count_b-1],Ingrid,Bob).transact({"from":Bob,"value":0})
  tx_receipt2 = web3.eth.wait_for_transaction_receipt(tx_hash2)
  # print("乐观情况下关闭支付通道的消耗:",tx_receipt.gasUsed + tx_receipt2.gasUsed)

# 关闭支付通道（悲观情况）
def close_lc_pessimistic(value):
  load_count_a = 1
  load_count_b = 1
  cvc_count_b = 2
  tx_hash = Channels.functions.submit_transaction_a(load_count_a,value,value,ec_Bob_hash[load_count_a-1],ec_Bob_v[load_count_a-1],
            ec_Bob_r[load_count_a-1],ec_Bob_s[load_count_a-1],30).transact({"from":Ingrid,"value":0})
  tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
  tx_hash1 = Channels.functions.check_cvc_Validity(ec_Ingrid_hash_cvc[cvc_count_b-1],ec_Ingrid_v_cvc[cvc_count_b-1],
            ec_Ingrid_r_cvc[cvc_count_b-1],ec_Ingrid_s_cvc[cvc_count_b-1]).transact({"from":Ingrid,"value":0})
  tx_receipt1 = web3.eth.wait_for_transaction_receipt(tx_hash1)
  tx_hash2 = Channels.functions.submit_transaction_b(load_count_b,value,value,ec_Ingrid_hash[load_count_b-1],
            ec_Ingrid_v[load_count_b-1],ec_Ingrid_r[load_count_b-1],ec_Ingrid_s[load_count_b-1],Ingrid,Bob).transact({"from":Bob,"value":0})
  tx_receipt2=web3.eth.wait_for_transaction_receipt(tx_hash2)
  # print("lc pessimistic closed cost : ",tx_receipt.gasUsed+tx_receipt1.gasUsed+tx_receipt2.gasUsed)

def get_balance(account):
  print(1)
  tx_hash=Channels.functions.getBalance1(account).call()
  tx_receipt=web3.eth.wait_for_transaction_receipt(tx_hash)
  # print(tx_receipt)

# 用于保存Ingrig和Bob链下信息的数组（跨链虚拟支付通道）
message_cvc = []
cvc_Ingrid_balance = 0
cvc_Bob_balance = 0
cvc_count = 0   # 指示message_cvc[]的数组下标
cvc_OpenMessage_Ingrid = []
sign_cvc_OpenMessage_Ingrid = [] # 保存ingrid签名后的信息
message_Bob_cvc = []
sign_cvc_OpenMessage_Bob = []
ec_Ingrid_hash_cvc = []
ec_Ingrid_v_cvc = []
ec_Ingrid_r_cvc = []
ec_Ingrid_s_cvc = []
ec_Bob_hash_cvc = []
ec_Bob_v_cvc = []
ec_Bob_r_cvc = []
ec_Bob_s_cvc = []

# 打开跨链的虚拟通道
def deploy_cvc(Ingrid,Bob,value,time_cvc):
  print("cvc open...")
  # 双方锁定的金额
  global cvc_Ingrid_balance
  global cvc_Bob_balance
  global cvc_count
  cvc_Ingrid_balance=value
  cvc_Bob_balance=value
  # 跨链虚拟通道的创建信息
  message_cvc.append("open a virtual channel with initial balance Ingrid"+str(cvc_Ingrid_balance)+"Bob"+str(cvc_Bob_balance))
  cvc_OpenMessage_Ingrid.append(encode_defunct(text=message_cvc[cvc_count]))
  # Ingrid对跨链虚拟通道的消息进行签名
  a = web3.eth.account.sign_message(cvc_OpenMessage_Ingrid[cvc_count],private_key=Ingrid_privateKey)
  sign_cvc_OpenMessage_Ingrid.append(a)
  b = web3.eth.account.recover_message(cvc_OpenMessage_Ingrid[cvc_count], signature ='0x36e5a520780a16f5804c8036c470f7a8938fca54768cce5d577a72e5a35c5df92befd39f50a826cf594c5555949b29913ad2076fe57a9801d11c54bd839aac161c')
  print("OpenMessage_cvc_Ingrid:",a)

  # 计算打开跨链虚拟通道消息的大小（Ingrid）
  # CVC_Open_Message_Signed_by_Ingrid_bytes = len(web3.toHex(sign_cvc_OpenMessage_Ingrid[cvc_count].signature))/2
  # print("CVC_Open_Message_Signed_by_Ingrid_hex",web3.toHex(sign_cvc_OpenMessage_Ingrid[cvc_count].signature))
  # print("CVC_Open_Message_Signed_by_Ingrid_bytes:",CVC_Open_Message_Signed_by_Ingrid_bytes)
  
  # 取出签名信息中的hash，v，r，s （主要传给智能合约进行验签，方便智能合约验签）
  ec_recover_args_a_cvc=(msghash,v,r,s)=(web3.toHex(sign_cvc_OpenMessage_Ingrid[cvc_count].messageHash),sign_cvc_OpenMessage_Ingrid[cvc_count].v,
            to_32byte_hex(sign_cvc_OpenMessage_Ingrid[cvc_count].r),to_32byte_hex(sign_cvc_OpenMessage_Ingrid[cvc_count].s))
  ec_Ingrid_hash_cvc.append(ec_recover_args_a_cvc[0])
  ec_Ingrid_v_cvc.append(ec_recover_args_a_cvc[1]) 
  ec_Ingrid_r_cvc.append(ec_recover_args_a_cvc[2])
  ec_Ingrid_s_cvc.append(ec_recover_args_a_cvc[3])

  # Bob对数据进行签名并保存于数组
  message_Bob_cvc.append(encode_defunct(text=message_cvc[cvc_count]))
  sign_cvc_OpenMessage_Bob.append(web3.eth.account.sign_message(message_Bob_cvc[cvc_count],private_key=Bob_privateKey))
  print("OpenMessage_cvc_Bob:",sign_cvc_OpenMessage_Bob[0])
  
  # 计算打开跨链虚拟通道消息的大小（Bob）
  # CVC_Open_Message_Signed_by_Bob_bytes = len(web3.toHex(sign_cvc_OpenMessage_Bob[cvc_count].signature))/2
  # print("CVC_Open_Message_Signed_by_Bob_hex",web3.toHex(sign_cvc_OpenMessage_Bob[cvc_count].signature))
  # print("CVC_Open_Message_Signed_by_Bob_bytes:",CVC_Open_Message_Signed_by_Bob_bytes)

  # 取出签名信息中的hash，v，r，s （主要传给智能合约进行验签，方便智能合约验签）
  ec_recover_args_b_cvc=(msghash,v,r,s)=(web3.toHex(sign_cvc_OpenMessage_Bob[cvc_count].messageHash),sign_cvc_OpenMessage_Bob[cvc_count].v,
            to_32byte_hex(sign_cvc_OpenMessage_Bob[cvc_count].r),to_32byte_hex(sign_cvc_OpenMessage_Bob[cvc_count].s))
  ec_Bob_hash_cvc.append(ec_recover_args_b_cvc[0])
  ec_Bob_v_cvc.append(ec_recover_args_b_cvc[1])
  ec_Bob_r_cvc.append(ec_recover_args_b_cvc[2])
  ec_Bob_s_cvc.append(ec_recover_args_b_cvc[3])
  # 将签名发送给智能合约
  # tx_hash=Channels.functions.open_cvc(ec_Ingrid_hash_cvc[0],ec_Ingrid_v_cvc[0],ec_Ingrid_r_cvc[0],ec_Ingrid_s_cvc[0],time_cvc,ec_Bob_hash_cvc[0],
  #           ec_Bob_v_cvc[0],ec_Bob_r_cvc[0],ec_Bob_s_cvc[0]).transact({"from":Ingrid,"value":value})
  # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)


# 更新虚拟通道，Ingrid和Bob链下更新消息，然后保存在数组中
def update_cvc(value):
  print("cvc update...")
  global cvc_count
  cvc_count=cvc_count+1
  message_cvc.append('Number:count'+str(cvc_count)+'accounta.balance:'+str(~value)+'accountb.balance:'+str(value))
  cvc_OpenMessage_Ingrid.append(encode_defunct(text=message_cvc[cvc_count]))
  sign_cvc_OpenMessage_Ingrid.append(web3.eth.account.sign_message(cvc_OpenMessage_Ingrid[cvc_count],private_key=Ingrid_privateKey))
  print("UpdateMessage_cvc_Ingrid:", sign_cvc_OpenMessage_Ingrid)
  ec_recover_args_a_cvc=(msghash,v,r,s)=(web3.toHex(sign_cvc_OpenMessage_Ingrid[cvc_count].messageHash),sign_cvc_OpenMessage_Ingrid[cvc_count].v,
            to_32byte_hex(sign_cvc_OpenMessage_Ingrid[cvc_count].r),to_32byte_hex(sign_cvc_OpenMessage_Ingrid[cvc_count].s))
  ec_Ingrid_hash_cvc.append(ec_recover_args_a_cvc[0])
  ec_Ingrid_v_cvc.append(ec_recover_args_a_cvc[1])
  ec_Ingrid_r_cvc.append(ec_recover_args_a_cvc[2])
  ec_Ingrid_s_cvc.append(ec_recover_args_a_cvc[3])
  message_Bob_cvc.append(encode_defunct(text=message_cvc[cvc_count]))
  sign_cvc_OpenMessage_Bob.append(web3.eth.account.sign_message(message_Bob_cvc[cvc_count],private_key=Bob_privateKey))
  print("UpdateMessage_cvc_Bob:", sign_cvc_OpenMessage_Bob)
  ec_recover_args_b_cvc=(msghash,v,r,s)=(web3.toHex(sign_cvc_OpenMessage_Bob[cvc_count].messageHash),sign_cvc_OpenMessage_Bob[cvc_count].v,
            to_32byte_hex(sign_cvc_OpenMessage_Bob[cvc_count].r),to_32byte_hex(sign_cvc_OpenMessage_Bob[cvc_count].s))
  ec_Bob_hash_cvc.append(ec_recover_args_b_cvc[0])
  ec_Bob_v_cvc.append(ec_recover_args_b_cvc[1])
  ec_Bob_r_cvc.append(ec_recover_args_b_cvc[2])
  ec_Bob_s_cvc.append(ec_recover_args_b_cvc[3])

# 正常情况下关闭虚拟通道，即Ingrid和Bob在链下更新消息即可
def close_cvc(value):
  update_lc(value=0)
  print("cvc close...")

# 有争议的情况下关闭跨链虚拟通道
def close_cvc_abnormal(committeeAddress,transactionId,Ingrid_and_Bob_Balance, zero, value):
  print("cvc close...")
  cvc_count_a=2
  # Ingrid向智能合约提交跨链虚拟支付通道的状态消息
  tx_hash=Channels.functions.close_cvc_abnormal(ec_Bob_hash_cvc[0],ec_Bob_v_cvc[0],ec_Bob_r_cvc[0],ec_Bob_s_cvc[0],ec_Ingrid_hash_cvc[cvc_count_a-1],
            ec_Ingrid_v_cvc[cvc_count_a-1],ec_Ingrid_r_cvc[cvc_count_a-1],ec_Ingrid_s_cvc[cvc_count_a-1]).transact({"from":Ingrid,"value":0})
  tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash) 
  # 启动委员会投票，判断Ingrid是否诚实
  print("voting...")
  committee(1,3000000000000000000)
  # 智能合约根据投票结果分配余额
  tx_hash1 = Channels.functions.close_cvc_abnormal_1(committeeAddress,transactionId,Ingrid_and_Bob_Balance,zero).transact({"from":Ingrid,"value":value})
  tx_receipt1 = web3.eth.wait_for_transaction_receipt(tx_hash1)
  # print("close_cvc_abnomal cost : ", tx_receipt.gasUsed+tx_receipt1.gasUsed)
  
  
# def close_cvc_abnormal_and_exchange_coins(Ingrid_and_Bob_Balance, zero, value):

# 进行委员会投票
def committee(transactionId,value):
  # 创建投票事件
  tx_hash1=commit.functions.createVote(transactionId,value).transact({"from":Voter_1,"value":0})
  tx_receipt1=web3.eth.wait_for_transaction_receipt(tx_hash1)
  # 成员交押金
  tx_hash2=commit.functions.pay().transact({"from":Voter_1,"value":value})
  tx_hash3=commit.functions.pay().transact({"from":Voter_2,"value":value})
  tx_hash4=commit.functions.pay().transact({"from":Voter_3,"value":value})
  tx_receipt2=web3.eth.wait_for_transaction_receipt(tx_hash2)
  tx_receipt3=web3.eth.wait_for_transaction_receipt(tx_hash3)
  tx_receipt4=web3.eth.wait_for_transaction_receipt(tx_hash4)
  # 进行投票
  tx_hash5=commit.functions.vote(Voter_1,1,transactionId).transact({"from":Voter_1,"value":0})
  tx_hash6=commit.functions.vote(Voter_2,1,transactionId).transact({"from":Voter_1,"value":0})
  tx_hash7=commit.functions.vote(Voter_3,1,transactionId).transact({"from":Voter_1,"value":0})
  tx_receipt5=web3.eth.wait_for_transaction_receipt(tx_hash5)
  tx_receipt6=web3.eth.wait_for_transaction_receipt(tx_hash6)
  tx_receipt7=web3.eth.wait_for_transaction_receipt(tx_hash7)
  # 获取投票结果
  tx_hash8=commit.functions.getVoteRes(transactionId).transact({"from":Voter_1,"value":0})
  tx_receipt8=web3.eth.wait_for_transaction_receipt(tx_hash8)
  res=commit.functions.getTrue(transactionId).call()
  print("voting_result:", res)
  # 惩罚
  # tx_hash9=commit.functions.punishment(transactionId).transact({"from":Voter_1,"value":0})
  # tx_receipt9=web3.eth.wait_for_transaction_receipt(tx_hash9)
  # print("commitee cost : ",tx_receipt1.gasUsed+tx_receipt2.gasUsed+tx_receipt3.gasUsed+tx_receipt4.gasUsed+tx_receipt5.gasUsed+
  #           tx_receipt6.gasUsed+tx_receipt7.gasUsed+tx_receipt8.gasUsed)
  return res


# 部署委员会合约：
committee_contract_address = Deployment_committee_contract()
print("committee_contract_address:",committee_contract_address)

# 委员会合约部署之后可以多次调用
for i in range (1):
  commit = web3.eth.contract(committee_contract_address, abi=abi_2)
  Deployment_channel_contract()
  deploy_lc(Ingrid,Bob,0)   # 构建账本通道
  deploy_cvc(Ingrid, Bob, 0, 0)    # 构建跨链虚拟通道
  update_cvc(0)   # 更新跨链虚拟通道
  # close_cvc(0)    # 正常关闭跨链虚拟通道
  close_cvc_abnormal(committee_contract_address,1,0,0,0)   # 非正常关闭跨链虚拟通道
  print("Cross-Chain virtual payment channel is closed")
  # update_lc(0)    # 更新账本通道
  # close_lc(0)   # 正常关闭账本通道
  # close_lc_pessimistic(0)   # 非正常关闭账本通道


















