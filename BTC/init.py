import bitcoinutils.setup as setup
import consts


def initNetwork():
    if setup.get_network() == None: 
        setup.setup(consts.network)
