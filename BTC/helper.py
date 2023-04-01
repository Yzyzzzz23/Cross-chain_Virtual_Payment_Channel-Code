import binascii
import hashlib
from bitcoinutils.transactions import Transaction
import random
import base58

random.seed(1)


def gen_secret() -> str:
    """
        Replace this method with a secure random generator
    """
    r = random.randrange(0, 255)  # INSECURE, just for demo
    r = hex(r)[2:]
    if len(r) == 1:
        return f'0{r}'
    return r


def hash256(hexstring: str) -> str:
    data = binascii.unhexlify(hexstring)
    h1 = hashlib.sha256(data)
    h2 = hashlib.sha256(h1.digest())
    return h2.hexdigest()


def print_tx(tx: Transaction, name: str) -> None:
    print(f'{name}: {int(len(tx.serialize()) / 2)} Bytes')
    print(tx.serialize())   # 转化为字符串
    print('----------------------------------')


def hex_to_base58(hex_string):
    if hex_string[:2] in ["0x", "0X"]:
        hex_string = "41" + hex_string[2:]
    bytes_str = bytes.fromhex(hex_string)
    base58_str = base58.b58encode_check(bytes_str)
    return base58_str.decode("UTF-8")


def base58_to_hex(base58_string):
    asc_string = base58.b58decode_check(base58_string)
    return asc_string.hex().upper()