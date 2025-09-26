"""Basic entity management module for Arkiv client."""

from typing import TYPE_CHECKING

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

    # TODO: Add entity management methods
    # - create_entity()
    # - get_entity()
    # - delete_entity()
    # - exists_entity()
