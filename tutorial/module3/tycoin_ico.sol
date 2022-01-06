// tycoin ICO

pragma solidity ^0.4.11

contract tycoin_ico {

    // introduce the maximum number of tycoin that available for sale
    uint public max_tycoin = 1000000;

    // USD to tycoin conversion rate
    uint public usd_to_tycoin = 1000;

    // the total number of tycoin that have been bought by investors
    uint public total_tycoin_bought = 0;

    // mapping from the investor address to its equity in tycoin and usd
    mapping(address => uint) equity_tycoins;
    mapping(address => uint) equity_usd;

    // check if an investor can buy tycoin
    modifier can_buy_tycoin(uint usd_invested) {
        require (usd_invested * usd_to_tycoin + total_tycoin_bought <= max_tycoin);
        _;
    }

    // get the equity in tycoin of an investors
    function equity_in_tycoin(address investor) external constant returns (uint) {
        return equity_tycoins[investor];
    }

    // get the equity in usd of an investors
    function equity_in_usd(address investor) external constant returns (uint) {
        return equity_usd[investor];
    }

    // buy tycoin
    function buy_tycoins(address investor, uint usd_invested) external 
    can_buy_tycoin(usd_invested) {
        uint tycoin_bought = usd_invested * usd_to_tycoin;
        equity_tycoins[investor] += tycoin_bought;
        equity_usd[investor] = equity_in_tycoin / usd_to_tycoin;
        total_tycoin_bought += tycoin_bought;
    }

    // sell tycoin
    function sell_tycoins(address investor, uint tycoin_to_sell) external {
        equity_tycoins[investor] -= tycoin_to_sell;
        equity_usd[investor] = equity_in_tycoin[investor] / usd_to_tycoin;
        total_tycoin_bought -= tycoin_to_sell;
    }

}