"""Tests for entity creation functionality in ArkivModule."""

import logging

from hexbytes import HexBytes
from web3.types import TxReceipt

from arkiv.client import Arkiv
from arkiv.smart_contract import STORAGE_ADDRESS
from arkiv.types import Operations
from arkiv.utils import to_create_operation, to_tx_params

logger = logging.getLogger(__name__)


class TestEntityCreate:
    """Test cases for create_entity function."""

    def test_create_entity_with_payload_web3(self, arkiv_client_http: Arkiv) -> None:
        """Test create_entity with custom payload checking against Web3 client behavior."""
        payload = b"Hello world!"
        btl = 60  # 60 blocks to live

        # Get the expected sender address from client's default account
        expected_from_address = arkiv_client_http.eth.default_account

        # Wrap in Operations container
        create_op = to_create_operation(payload=payload, btl=btl)
        operations = Operations(creates=[create_op])

        # Convert to transaction parameters and send
        tx_params = None  # Use default tx params
        tx_params = to_tx_params(operations, tx_params)
        tx_hash = arkiv_client_http.eth.send_transaction(tx_params)

        logger.info(f"Transaction hash: {tx_hash.to_0x_hex()}")

        # Basic transaction hash validation
        assert tx_hash is not None
        assert isinstance(tx_hash, HexBytes)
        assert len(tx_hash) == 32  # Hash length in bytes

        # Wait for transaction confirmation
        tx_receipt: TxReceipt = arkiv_client_http.eth.wait_for_transaction_receipt(
            tx_hash
        )
        logger.info(f"Transaction confirmed in block {tx_receipt['blockNumber']}")
        logger.info(f"Gas used: {tx_receipt['gasUsed']}")
        logger.info(
            f"Transaction status: {'SUCCESS' if tx_receipt['status'] == 1 else 'FAILED'}"
        )

        # Verify transaction was successful
        assert tx_receipt["status"] == 1, "Transaction should have succeeded"

        # Verify transaction was included in a block
        assert tx_receipt["blockNumber"] is not None, "Transaction should be in a block"
        assert tx_receipt["blockNumber"] > 0, "Block number should be positive"

        # Verify gas was consumed (entity creation should use gas)
        assert tx_receipt["gasUsed"] > 0, "Transaction should have consumed gas"

        # Verify transaction hash matches
        assert tx_receipt["transactionHash"] == tx_hash, (
            "Receipt hash should match transaction hash"
        )

        # Get the actual transaction details for further validation
        tx_details = arkiv_client_http.eth.get_transaction(tx_hash)
        logger.info(f"Transaction from: {tx_details['from']}")
        logger.info(f"Transaction to: {tx_details['to']}")
        logger.info(f"Transaction value: {tx_details['value']}")

        # Verify transaction sender matches the current signer
        assert tx_details["from"] == expected_from_address, (
            f"Transaction sender should be {expected_from_address}, got {tx_details['from']}"
        )

        # Verify transaction was sent to the correct Arkiv storage contract
        assert tx_details["to"] == STORAGE_ADDRESS, (
            f"Transaction should be sent to Arkiv storage contract {STORAGE_ADDRESS}, got {tx_details['to']}"
        )

        # Verify transaction value is 0 (no ETH should be sent)
        assert tx_details["value"] == 0, "Entity creation should not send ETH"

        # Verify transaction contains data (RLP-encoded operations)
        # Some blockchain implementations may use 'input' instead of 'data'
        tx_data = tx_details.get("data") or tx_details.get("input")
        assert tx_data is not None, "Transaction should contain data or input field"
        assert len(tx_data) > 0, "Transaction data should not be empty"
        assert tx_data != "0x", "Transaction data should contain encoded operations"
        logger.info(f"Transaction data length: {len(tx_data)} bytes")

        logger.info("Entity creation successful")
