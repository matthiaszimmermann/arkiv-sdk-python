"""Basic entity management module for Arkiv client."""

from typing import TYPE_CHECKING

from hexbytes import HexBytes
from web3.types import TxParams

from .types import AnnotationValue, Operations
from .utils import to_create_operation, to_tx_params

# Deal with potential circular imports between client.py and module.py
if TYPE_CHECKING:
    from .client import Arkiv


class ArkivModule:
    """Basic Arkiv module for entity management operations."""

    def __init__(self, client: "Arkiv") -> None:
        """Initialize Arkiv module with client reference."""
        self.client = client

    def is_available(self) -> bool:
        """Check if Arkiv functionality is available."""
        return True

    def create_entity(
        self,
        payload: bytes | None = None,
        annotations: dict[str, AnnotationValue] | None = None,
        btl: int = 0,
        tx_params: TxParams | None = None,
    ) -> HexBytes:
        """
        Create a new entity on the Arkiv storage contract.

        Args:
            payload: Optional data payload for the entity
            annotations: Optional key-value annotations
            btl: Blocks to live (default: 0)
            tx_params: Optional additional transaction parameters

        Returns:
            Transaction hash of the create operation
        """
        # Create the operation
        create_op = to_create_operation(
            payload=payload, annotations=annotations, btl=btl
        )

        # Wrap in Operations container
        operations = Operations(creates=[create_op])

        # Convert to transaction parameters and send
        tx_params = to_tx_params(operations, tx_params)
        tx_hash = self.client.eth.send_transaction(tx_params)

        return tx_hash
