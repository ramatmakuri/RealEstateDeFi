pragma solidity ^0.5.5;

contract SmartInvoice {
  uint public invoiceAmount;
  address payable owner;//this will be the address that the money is being sent to  
    address payable renter;

    constructor(uint _invoiceAmount, address payable account1, address payable account2) public {
    invoiceAmount = _invoiceAmount;
    owner = account1;
    renter = account2;
    owner = msg.sender; 

  }
    function () external payable{
    require(msg.value == invoiceAmount,"Payment should be the invoiced amount.");
    }
  function getContractBalance() public view returns(uint) {
    return address(this).balance;
  }

  function withdraw() public {
    require(
      msg.sender == owner,
      "Only the owner of the address can withdraw the payment."
    );
    msg.sender.transfer(address(this).balance);
  }

  function payOwner() public payable{
    require(msg.sender == renter);
    require(msg.value == invoiceAmount);
    renter.transfer(invoiceAmount);
  }
}