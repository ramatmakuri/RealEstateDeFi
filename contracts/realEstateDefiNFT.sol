pragma solidity >=0.5.5 < 0.6.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract RegisterRE is ERC721Full {
    constructor() public ERC721Full("RegisterREAL", "REAL") {}

    struct realST {
        string name;
        string propertyAddress;
        uint256 appraisalValue;
    }
    mapping(uint256 => realST) public realMapp;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerRealEstate(
        address owner,
        string memory name,
        string memory propertyAddress,
        uint256 appraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        realMapp[tokenId] = realST(name, propertyAddress, appraisalValue);
        return tokenId;
    }
    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) public returns (uint256) {
        realMapp[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return realMapp[tokenId].appraisalValue;
    }
}


