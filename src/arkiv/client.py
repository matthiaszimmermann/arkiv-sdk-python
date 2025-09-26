"""Arkiv client - extends Web3 with entity management."""

from typing import Any

from web3 import Web3
from web3.providers.base import BaseProvider

from .entities import ArkivModule


class Arkiv(Web3):
    """
    Arkiv client that extends Web3 with entity management capabilities.

    Provides the familiar Web3.py interface plus arkiv.* methods for entity operations.
    """

    def __init__(self, provider: BaseProvider | None = None, **kwargs: Any) -> None:
        """Initialize Arkiv client with Web3 provider."""
        super().__init__(provider, **kwargs)

        # Initialize entity management module
        self.arkiv = ArkivModule(self)

    def __repr__(self) -> str:
        """String representation of Arkiv client."""
        return f"<Arkiv connected={self.is_connected()}>"
