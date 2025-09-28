"""Constants used in the Arkiv SDK."""

from collections.abc import Sequence
from typing import Any, Final

from eth_typing import ChecksumAddress
from web3 import Web3

STORAGE_ADDRESS: Final[ChecksumAddress] = Web3.to_checksum_address(
    "0x0000000000000000000000000000000060138453"
)

STORAGE_ABI: Final[Sequence[dict[str, Any]]] = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "entityKey", "type": "uint256"},
            {"indexed": False, "name": "expirationBlock", "type": "uint256"},
        ],
        "name": "GolemBaseStorageEntityCreated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "entityKey", "type": "uint256"},
            {"indexed": False, "name": "expirationBlock", "type": "uint256"},
        ],
        "name": "GolemBaseStorageEntityUpdated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": True, "name": "entityKey", "type": "uint256"}],
        "name": "GolemBaseStorageEntityDeleted",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "entityKey", "type": "uint256"},
            {"indexed": False, "name": "oldExpirationBlock", "type": "uint256"},
            {"indexed": False, "name": "newExpirationBlock", "type": "uint256"},
        ],
        "name": "GolemBaseStorageEntityBTLExtended",
        "type": "event",
    },
]
