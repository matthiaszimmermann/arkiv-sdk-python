"""Tests for basic Arkiv client functionality and arkiv module availability."""

import logging

from arkiv import Arkiv
from arkiv.entities import ArkivModule

logger = logging.getLogger(__name__)


def test_arkiv_client_extends_web3(arkiv_client_http: Arkiv) -> None:
    """Test that Arkiv client properly extends Web3 functionality."""
    # Should have all Web3 attributes
    assert hasattr(arkiv_client_http, "eth"), "Should have eth module"
    assert hasattr(arkiv_client_http, "net"), "Should have net module"
    assert hasattr(arkiv_client_http, "is_connected"), "Should have is_connected method"

    # Should be connected
    assert arkiv_client_http.is_connected(), "Should be connected to node"

    logger.info("✅ Arkiv client properly extends Web3")


def test_arkiv_client_has_arkiv_module(arkiv_client_http: Arkiv) -> None:
    """Test that Arkiv client has the arkiv module available."""
    assert hasattr(arkiv_client_http, "arkiv"), "Arkiv client should have arkiv module"

    arkiv_module = arkiv_client_http.arkiv
    assert arkiv_module is not None, "Arkiv module should not be None"
    assert isinstance(arkiv_module, ArkivModule), "Should be ArkivModule instance"

    # Test availability check
    is_available = arkiv_module.is_available()
    assert isinstance(is_available, bool), "is_available should return boolean"
    assert is_available is True, "Arkiv module should be available"

    logger.info("✅ Arkiv module is available")


def test_arkiv_client_repr(arkiv_client_http: Arkiv) -> None:
    """Test Arkiv client string representation."""
    repr_str = repr(arkiv_client_http)
    assert isinstance(repr_str, str), "repr should return string"
    assert "Arkiv" in repr_str, "repr should contain 'Arkiv'"
    assert "connected=" in repr_str, "repr should show connection status"

    logger.info(f"✅ Arkiv client repr: {repr_str}")


def test_arkiv_module_has_client_reference(arkiv_client_http: Arkiv) -> None:
    """Test that arkiv module has reference to parent client."""
    arkiv_module = arkiv_client_http.arkiv

    assert hasattr(arkiv_module, "client"), "Arkiv module should have client reference"
    assert (
        arkiv_module.client is arkiv_client_http
    ), "Client reference should point to parent"

    logger.info("✅ Arkiv module has proper client reference")
