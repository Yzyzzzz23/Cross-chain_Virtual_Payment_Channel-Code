// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
contract committee{
    struct committeeman{
        address payable committeemanAddress;
        uint vote_res;
    }
    struct committeeNumber{
       uint vote_count;
       uint f; 
       uint intermediary_count;
    }
    address committeeNumberAddress;
    mapping(address=>committeeNumber) committeemap;

    struct voteEvent{
        uint transactionId;
        uint vote_true;
        uint vote_false;
        uint vote_res;
        uint committeemanAmount;
        uint cash;
        mapping (uint => committeeman) map;
    }
    //  向合约地址转账
    function pay() payable public{          
    }
    // 获取合约地址余额
    function getBalance() view public returns(uint){
        return address(this).balance;
    }
    uint voteAmount;
    mapping(uint=>voteEvent) votemap;
    // 选择中间人
    function chooseIntermediary(address intermediaryAddress) public{
        committeeNumber storage _committeeNumber = committeemap[intermediaryAddress];
        _committeeNumber.intermediary_count++;
    }
    // 获取指定人的f值
    function getF(address addr) public returns(uint){
        committeeNumber storage _committeeNumber = committeemap[addr];
        _committeeNumber.f=_committeeNumber.vote_count/_committeeNumber.intermediary_count;
        return _committeeNumber.f;
    }
    function getf(address addr) view public returns(uint){
        committeeNumber storage _committeeNumber = committeemap[addr];
        return _committeeNumber.f;
    }
    // 创建投票
    function createVote(uint _transactionId,uint _cash) public{
        voteAmount = _transactionId;
        voteEvent storage n = votemap[voteAmount];
        n.transactionId = _transactionId;
        n.vote_true = 0;
        n.vote_false = 0;
        n.committeemanAmount = 0;
        n.cash=_cash;
    }
    // 投票
    function vote(address payable _committeemanAddress, uint vote_res,uint _transactionId) public{
        voteEvent storage _voteEvent = votemap[_transactionId];
        committeeNumber storage _committeeNumber = committeemap[_committeemanAddress];
        _committeeNumber.vote_count=_committeeNumber.vote_count+1;
        if(vote_res == 1){
            _voteEvent.vote_true++;
        }
        else if(vote_res == 0){
            _voteEvent.vote_false++;
        }
        _voteEvent.committeemanAmount++;
        _voteEvent.map[_voteEvent.committeemanAmount] = committeeman(_committeemanAddress,vote_res);
    }
    // 返回投票结果
    function getTrue(uint _transactionId) view public returns(uint){
        voteEvent storage _voteEvent = votemap[_transactionId];
        return _voteEvent.transactionId;
    }
    // 获取投票结果，因为不能返回值，返回值用上面的函数
    function getVoteRes(uint _transactionId) public {
        voteEvent storage _voteEvent = votemap[_transactionId];
        if(_voteEvent.vote_true>_voteEvent.vote_false){
            _voteEvent.vote_res=1;
        }
        else{
            _voteEvent.vote_res=0;
        }
    }
    // 惩罚和分配金额
    function punishment(uint _transactionId) public {
        uint amount;
        uint each;
        voteEvent storage _voteEvent = votemap[_transactionId];
        amount = _voteEvent.committeemanAmount * _voteEvent.cash;
        if(_voteEvent.vote_res == 1){
            each = amount/_voteEvent.vote_true;
            for(uint i=1;i<=_voteEvent.committeemanAmount;i++){
                if(_voteEvent.map[i].vote_res == 1){
                    _voteEvent.map[i].committeemanAddress.transfer(each);
                    // addr.transfer(450000000000000000);
                }
            }
        }
        else{
            each = amount/_voteEvent.vote_false;
            for(uint i=1;i<=_voteEvent.committeemanAmount;i++){
                if(_voteEvent.map[i].vote_res == 0){
                    _voteEvent.map[i].committeemanAddress.transfer(each);
                }
            }
        }
    }
}
