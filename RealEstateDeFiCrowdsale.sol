pragma solidity >=0.5.0 <0.6.0;

import "./RealEstateDeFiToken.sol";
import "./RealEstateDeFiCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundableCrowdsale.sol";

// Have the RalEstateCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale

contract RealEstateCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, TimedCrowdsale, RefundableCrowdsale { // UPDATE THE CONTRACT SIGNATURE TO ADD INHERITANCE
    using SafeMath for uint256;
    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint rate,
        address payable wallet,
        realEstateDefi token,
        uint cap,
        uint start_time,
        uint end_time,
        uint refundable_cap
        )   
        // YOUR CODE HERE!
        Crowdsale(rate, wallet, token) 
        CappedCrowdsale(cap)
        TimedCrowdsale (start_time, end_time)
        RefundableCrowdsale (refundable_cap)
        public {
        // constructor can stay empty
        }

}


contract RealEstateCrowdsaleDeployer {
    // Create an `address public` variable called `realestate_token_address`.
    // YOUR CODE HERE!
    address public realestate_token_address;
    // Create an `address public` variable called `realestate_crowdsale_address`.
    // YOUR CODE HERE!
    address public realestate_crowdsale_address;


    // Add the constructor.
    constructor(
       // YOUR CODE HERE!
       
       string memory name, 
       string memory symbol,
       uint initial_supply,
       uint rate,
       address payable wallet,
       uint cap,
       uint start_time,
       uint end_time,
       uint refundable_cap
       ) 
       public {
        // Create a new instance of the KaseiCoin contract.
        // YOUR CODE HERE!
        realEstateDefi token = new realEstateDefi (name, symbol,initial_supply);
        // Assign the token contract’s address to the `kasei_token_address` variable.
        // YOUR CODE HERE!
        realestate_token_address = address(token);
        // Create a new instance of the `KaseiCoinCrowdsale` contract
        // YOUR CODE HERE!
        RealEstateCrowdsale realestate_crowd_sale = new RealEstateCrowdsale (
            rate, 
            wallet, 
            token, 
            cap, 
            start_time, 
            end_time, 
            refundable_cap);
        // Aassign the `KaseiCoinCrowdsale` contract’s address to the `kasei_crowdsale_address` variable.
        // YOUR CODE HERE!
        realestate_crowdsale_address = address(realestate_crowd_sale);  
        // Set the `KaseiCoinCrowdsale` contract as a minter
        // YOUR CODE HERE!
        token.addMinter(realestate_crowdsale_address);
	// Have the `KaseiCoinCrowdsaleDeployer` renounce its minter role.
        // YOUR CODE HERE!
        token.renounceMinter();
        
    } 
}