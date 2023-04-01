pragma solidity 0.8.0;

contract Payment{
    struct Partner{
        address addr;
        uint balance;
    }

    struct Signature{
        uint8 v;
        bytes32 r;
        bytes32 s;
    }

    struct Man{
        string name;
        uint8 age;
    }



    Partner Bob = Partner(address(0x0a512C35AbFA13428a6C6CdD0C347aE7874Ff0aa), 100);
    Partner Ingrid = Partner(address(0xC9b9F506F45356ea2E5c7BC8f7303Dc82E97f616), 100);

    mapping(address => bool) public partners;
    mapping(address => bool) public members_;


    uint sequence;
    uint fee;
    uint channelTime;
    uint waitRounds;
    uint delayTransfer;
    bool subOp2;

    mapping (address => bool) public members;

    constructor() public{
        subOp2 = false;
        channelTime = block.timestamp + 5 days;
        waitRounds = 10 hours;
        delayTransfer = 1 days;
        partners[Bob.addr] = true;
        partners[Ingrid.addr] = true;

        members[address(0x2eCcc99c951538F3acc0a470c1833c430DC4C63F)]=true;
        members[address(0x6Be3ebEe0e105C1c404599bd52a6a714dB767eB5)]=true;
        members[address(0x1AbB05903dA93668B031b55Cc21146F0bBb7154d)]=true;
        members[address(0xb88b29d5C82D9b9067e443934A19aDd2859602fA)]=true;
        members[address(0x31772F29C6274F4b120FBc3534A15B0adD220E06)]=true;
        sequence = 0;
        fee = 10;
    }




    function addrContains(address addr) public view returns (bool result) {
        result = members[addr];
    }


    function uploadMemSigs(Signature[] memory man) public payable returns(bool){
        return false;
    }

    function subOperation2(uint balanceBob, uint balanceIngrid, bytes32 O_CVPCh, Signature memory signatureB, Signature memory signatureI, bytes32 TXh, Signature[] memory memSigs) public payable
  returns (bool){

        bool result = true;
        if (block.timestamp < channelTime){
            return false;
        }

        address addrBob_ = ecr(O_CVPCh, signatureB.v, signatureB.r, signatureB.s);
        result = partners[addrBob_];

        address addrIngrid_ = ecr(O_CVPCh, signatureI.v, signatureI.r, signatureI.s);
        result = partners[addrIngrid_];

        if (result == false){
            return false;
        }

        if ((block.timestamp - channelTime) < waitRounds)
            return false;

        address[] memory memAddr = new address[](5);
        uint count = 0;

        for(uint j = 0; j<5; j++){
            Signature memory memSig = memSigs[j];
            address addr_ = ecr(TXh, memSig.v, memSig.r, memSig.s);
            if(members_[addr_]==false && members[addr_]==true){
                count = count + 1;
                members_[addr_]=true;
            }
        }

        if(count >= 3){
            Ingrid.balance = balanceIngrid;
            Ingrid.balance += Ingrid.balance + fee;
            Bob.balance = balanceBob;
            fee = 0;
        }else{
            Bob.balance = Bob.balance + Ingrid.balance;
            Ingrid.balance = 0;
            fee = 0;
        }
        subOp2 = true;

        return result;
    }


    function subOperation3(uint balanceBob, uint balanceIngrid, bytes32 O_CVPCh, Signature memory signatureB, Signature memory signatureI) public payable
  returns (bool){
        if(subOp2 == false){
          return false;
        }

        if ((block.timestamp - channelTime) < delayTransfer){
            return false;
        }

        address addrBob_ = ecr(O_CVPCh, signatureB.v, signatureB.r, signatureB.s);
        bool result = partners[addrBob_];

        if(result == false){
            return false;
        }

        address addrIngrid_ = ecr(O_CVPCh, signatureI.v, signatureI.r, signatureI.s);
        result = partners[addrIngrid_];

        if(result == false){
            return false;
        }

        Ingrid.balance = balanceIngrid;
        Bob.balance = balanceBob;
        return true;

    }



    function ecr (bytes32 msgh, uint8 v, bytes32 r, bytes32 s) public pure
  returns (address sender) {
    return ecrecover(msgh, v, r, s);
  }
}