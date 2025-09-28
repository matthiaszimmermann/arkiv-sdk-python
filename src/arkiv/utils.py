"""Utility methods."""

import logging

import rlp  # type: ignore[import-untyped]
from web3 import Web3
from web3.types import TxParams

from .smart_contract import STORAGE_ADDRESS
from .types import (
    Annotation,
    AnnotationValue,
    CreateOp,
    Operations,
)

logger = logging.getLogger(__name__)


def to_create_operation(
    payload: bytes | None = None,
    annotations: dict[str, AnnotationValue] | None = None,
    btl: int = 0,
) -> CreateOp:
    """
    Build a CreateOp for creating a single entity.

    Args:
        payload: Optional entity data payload
        annotations: Optional key-value annotations
        btl: Blocks to live (default: 0)

    Returns:
        CreateOp object ready to be used in Operations
    """
    # Ensure we have valid data
    if not payload:
        payload = b""

    # Separate string and numeric annotations
    string_annotations, numeric_annotations = split_annotations(annotations)

    # Build and return CreateOp
    return CreateOp(
        data=payload,
        btl=btl,
        string_annotations=string_annotations,
        numeric_annotations=numeric_annotations,
    )


def to_tx_params(
    operations: Operations,
    tx_params: TxParams | None = None,
) -> TxParams:
    """
    Convert Operations to TxParams for Arkiv contract interaction.

    Args:
        operations: Arkiv operations to encode
        tx_params: Optional additional transaction parameters

    Returns:
        TxParams ready for Web3.py transaction sending to Arkiv storage contract

    Note: 'to', 'value', and 'data' from tx_params will be overridden.
    """
    if not tx_params:
        tx_params = {}

    # Merge provided tx_params with encoded transaction data
    tx_params |= {
        "to": STORAGE_ADDRESS,
        "value": Web3.to_wei(0, "ether"),
        "data": rlp_encode_transaction(operations),
    }

    return tx_params


def rlp_encode_transaction(tx: Operations) -> bytes:
    """Encode a transaction in RLP."""

    def format_annotation(annotation: Annotation) -> tuple[str, AnnotationValue]:
        return (annotation.key, annotation.value)

    # Turn the transaction into a list for RLP encoding
    payload = [
        # Create
        [
            [
                element.btl,
                element.data,
                list(map(format_annotation, element.string_annotations)),
                list(map(format_annotation, element.numeric_annotations)),
            ]
            for element in tx.creates
        ],
        # Update
        [
            [
                element.entity_key,
                element.btl,
                element.data,
                list(map(format_annotation, element.string_annotations)),
                list(map(format_annotation, element.numeric_annotations)),
            ]
            for element in tx.updates
        ],
        # Delete
        [
            [
                element.entity_key,
            ]
            for element in tx.deletes
        ],
        # Extend
        [
            [
                element.entity_key,
                element.number_of_blocks,
            ]
            for element in tx.extensions
        ],
    ]
    logger.debug("Payload: %s", payload)
    encoded: bytes = rlp.encode(payload)
    logger.debug("Encoded payload: %s", encoded)
    return encoded


def split_annotations(
    annotations: dict[str, AnnotationValue] | None = None,
) -> tuple[list[Annotation], list[Annotation]]:
    """Helper to split mixed annotations into string and numeric lists."""
    string_annotations = []
    numeric_annotations = []

    if annotations:
        for key, value in annotations.items():
            annotation = Annotation(key=key, value=value)
            if isinstance(value, str):
                string_annotations.append(annotation)
            elif isinstance(value, int):
                numeric_annotations.append(annotation)

    return string_annotations, numeric_annotations
