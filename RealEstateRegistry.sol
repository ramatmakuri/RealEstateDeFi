pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract RealEstateRegistry is ERC721Full {
    constructor() public ERC721Full("RealEstateRegistryToken", "RealEstate") {}

    struct RealEstate {
        string name;
        string propertyAddress;
        uint256 appraisalValue;
    }

    mapping(uint256 => RealEstate) public RealEstateCollection;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerRealEstate(
        address owner,
        string memory name,
        string memory propertyAddress,
        uint256 initialAppraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        RealEstateCollection[tokenId] = RealEstate(name, propertyAddress, initialAppraisalValue);

        return tokenId;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) public returns (uint256) {
        RealEstateCollection[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return RealEstateCollection[tokenId].appraisalValue;
    }
}
