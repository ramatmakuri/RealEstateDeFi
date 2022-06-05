import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

file_path = Path("./SAMPLE.env")
load_dotenv(file_path)

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)

def load_nftcontract():

    # Load the contract ABI for NFT
    with open(Path('./contracts/compiled/realEstateDefiNFT_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_nftcontract()

def load_crowdsale_contract():
    # Load the contract ABI for NFT
    with open(Path('./contracts/compiled/realEstateDefiCS_abi.json')) as f:
        contract_cs_abi = json.load(f)
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS_CS")

    # Get the contract
    contractCS = w3.eth.contract(
        address=contract_address,
        abi=contract_cs_abi
    )

    return contractCS

# Load the contract
contract = load_nftcontract()
contractCS = load_crowdsale_contract()


################################################################################
# Helper functions to pin files and json to Pinata
################################################################################

def pin_realEstate(realestate_name, realestate_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(realestate_file.getvalue())

    # Build a token metadata file for the realestate
    token_json = {
        "name": realestate_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


st.title("Real Estate Appraisal System")
page_names = ['Register RealEstate', 'Invest in RealEstate', 'Check Investor Balances']
page = st.radio ('Select one:', page_names)

if page == 'Register RealEstate':
    st.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = st.selectbox("Select Account", options=accounts)
    st.markdown("---")
    ################################################################################
    # Register New RealEstate
    ################################################################################
    st.markdown("## Register New RealEstate")
    realEstate_name = st.text_input("Enter the name of the RealEstate")
    propertyAddress = st.text_input("Enter the property address")
    appraisalValue = st.text_input("Enter the initial appraisal amount")
    file = st.file_uploader("Upload RealEstate", type=["jpg", "jpeg", "png", "pdf"])
    if st.button("Register RealEstate"):
        realEstate_ipfs_hash = pin_realEstate(realEstate_name, file)
        realEstate_uri = f"ipfs/{realEstate_ipfs_hash}"
        tx_hash = contract.functions.registerRealEstate(
            address,
            realEstate_name,
            propertyAddress,
            int(appraisalValue),
            realEstate_uri
            ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[RealEstate IPFS Gateway Link](https:gateway.pinata.cloud/{realEstate_uri})")
        st.markdown("---")
    ################################################################################
    # Appraise Real Estate  
    ################################################################################
        st.markdown("## Appraise realEstate")
        tokens = contract.functions.totalSupply().call()
        token_id = st.selectbox("Choose an realEstate Token ID", list(range(tokens)))
        new_appraisal_value = st.text_input("Enter the new appraisal amount")
        appraisal_report_content = st.text_area("Enter details for the Appraisal Report")
        if st.button("Appraise Artwork"):

            # Use Pinata to pin an appraisal report for the report URI
            appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content)
            report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

            # Use the token_id and the report_uri to record the appraisal
            tx_hash = contract.functions.newAppraisal(
                token_id,
                int(new_appraisal_value),
                report_uri
            ).transact({"from": w3.eth.accounts[0]})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
        st.markdown("---")

    ################################################################################
    # Get Appraisals
    ################################################################################
        st.markdown("## Get the appraisal report history")
        art_token_id = st.number_input("realEstate ID", value=0, step=1)
        if st.button("Get Appraisal Reports"):
            appraisal_filter = contract.events.Appraisal.createFilter(
                fromBlock=0, argument_filters={"tokenId": art_token_id}
            )
            reports = appraisal_filter.get_all_entries()
            if reports:
                for report in reports:
                    report_dictionary = dict(report)
                    st.markdown("### Appraisal Report Event Log")
                    st.write(report_dictionary)
                    st.markdown("### Pinata IPFS Report URI")
                    report_uri = report_dictionary["args"]["reportURI"]
                    report_ipfs_hash = report_uri[7:]
                    st.markdown(
                        f"The report is located at the following URI: "
                        f"{report_uri}"
                    )
                    st.write("You can also view the report URI with the following ipfs gateway link")
                    st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
                    st.markdown("### Appraisal Event Details")
                    st.write(report_dictionary["args"])
            else:
                st.write("This artwork has no new appraisals")

if page == 'Invest in RealEstate':
    st.title("Invest in Decentralized Real Estate Financing")
    st.write("Choose an account to get started")
    accounts = w3.eth.accounts 
    investor_address = st.selectbox("Select Account", options=accounts)
    st.markdown("---")
    st.write("Choose an amount to continue")
    weiAmount = int(st.number_input("Enter the number of tokens you will like to buy"))
    if weiAmount > 0:
        #ContractInterface.methods.contractmethod(parameter).send({from: accounts[0],value : "amount in ether or wei"});    
        wallet = investor_address
        tx_hash_invest = contractCS.functions.buyTokens(wallet).transact({'from': investor_address, 'gas': 1000000, 'value': weiAmount})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash_invest)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown("---")

###if page == 'Check Investor Balances':
   ### st.title("Invest in Decentralized Real Estate Financing")
    #st.write("Choose an account to get started")
    #accounts = w3.eth.accounts 
    #investor_address = st.selectbox("Select Account", options=accounts)
    #st.markdown("---")
    #if st.button("balance"):
     #    tx_hash =  return(contractCS.functions.weiRaised().transact({'from': investor_address, 'gas': 1000000}))
      #   abc = return tx_hash
       #  st.write(return)
        # st.markdown("---")
        
        



