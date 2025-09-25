"""Tests for Web3.py client functionality with Arkiv nodes."""

import logging

from web3 import Web3

logger = logging.getLogger(__name__)


def test_web3_connection(web3_client_http: Web3) -> None:
    """Test that Web3 client is connected and responsive."""
    assert web3_client_http.is_connected(), "Web3 client should be connected"
    logger.info("Web3 connection verified")


def test_web3_chain_id(web3_client_http: Web3) -> None:
    """Test retrieving chain ID from the node."""
    chain_id = web3_client_http.eth.chain_id
    assert isinstance(chain_id, int), "Chain ID should be an integer"
    assert chain_id > 0, "Chain ID should be positive"

    logger.info(f"Chain ID: {chain_id}")


def test_web3_block_number(web3_client_http: Web3) -> None:
    """Test retrieving current block number."""
    block_number = web3_client_http.eth.block_number
    assert isinstance(block_number, int), "Block number should be an integer"
    assert block_number >= 0, "Block number should be non-negative"

    logger.info(f"Current block number: {block_number}")


def test_web3_get_block(web3_client_http: Web3) -> None:
    """Test retrieving block information."""
    # Get the latest block
    latest_block = web3_client_http.eth.get_block("latest")

    assert latest_block is not None, "Should retrieve latest block"
    assert "number" in latest_block, "Block should have number field"
    assert "hash" in latest_block, "Block should have hash field"
    assert "timestamp" in latest_block, "Block should have timestamp field"

    block_number = latest_block["number"]
    logger.info(f"Latest block: {block_number} ({latest_block['hash'].hex()})")


def test_web3_accounts(web3_client_http: Web3) -> None:
    """Test retrieving available accounts."""
    accounts = web3_client_http.eth.accounts
    assert isinstance(accounts, list), "Accounts should be a list"

    logger.info(f"Available accounts: {len(accounts)}")

    # If we have accounts, test balance retrieval
    if accounts:
        first_account = accounts[0]
        balance = web3_client_http.eth.get_balance(first_account)
        assert isinstance(balance, int), "Balance should be an integer (wei)"
        logger.info(f"Account {first_account[:10]}... balance: {balance} wei")


def test_web3_gas_price(web3_client_http: Web3) -> None:
    """Test retrieving current gas price."""
    gas_price = web3_client_http.eth.gas_price
    assert isinstance(gas_price, int), "Gas price should be an integer (wei)"
    assert gas_price >= 0, "Gas price should be non-negative"

    logger.info(f"Current gas price: {gas_price} wei")


def test_web3_net_version(web3_client_http: Web3) -> None:
    """Test retrieving network version."""
    net_version = web3_client_http.net.version
    assert isinstance(net_version, str), "Network version should be a string"
    assert len(net_version) > 0, "Network version should not be empty"

    logger.info(f"Network version: {net_version}")


def test_web3_client_version(web3_client_http: Web3) -> None:
    """Test retrieving client version information."""
    client_version = web3_client_http.client_version
    assert isinstance(client_version, str), "Client version should be a string"
    assert len(client_version) > 0, "Client version should not be empty"

    logger.info(f"Client version: {client_version}")
