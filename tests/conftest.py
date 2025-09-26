"""
Pytest configuration and fixtures for blockchain testing.

Provides either external node connections (via env vars) or containerized test nodes.
"""

import logging
import os
from collections.abc import Generator
from pathlib import Path

import pytest
from testcontainers.core.container import DockerContainer
from web3 import Web3

from arkiv import Arkiv

from .node_container import create_container_node

logger = logging.getLogger(__name__)


def _load_env_if_available() -> None:
    """Load .env file if dotenv is available and file exists."""
    try:
        from dotenv import load_dotenv

        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
            logger.info("Loaded environment variables from .env")
    except ImportError:
        logger.debug("python-dotenv not available, using system environment only")


# Load environment on import
_load_env_if_available()


@pytest.fixture(scope="session")
def arkiv_node() -> Generator[tuple[DockerContainer | None, str, str], None, None]:
    """
    Provide Arkiv node connection details.

    Returns:
        Tuple of (container, http_url, ws_url)
        - container is None for external nodes
    """
    # Try external node first
    rpc_url = os.getenv("RPC_URL")
    ws_url = os.getenv("WS_URL")

    if rpc_url and ws_url:
        logger.info(f"Using external node: {rpc_url}")
        yield None, rpc_url, ws_url
        return

    # Fall back to containerized node
    logger.info("Using containerized node")
    yield from create_container_node()


@pytest.fixture(scope="session")
def web3_client_http(arkiv_node: tuple[DockerContainer | None, str, str]) -> Web3:
    """
    Provide Web3 client connected to HTTP endpoint.

    Returns:
        Web3 client instance connected to the arkiv node
    """
    _, http_url, _ = arkiv_node
    client = Web3(Web3.HTTPProvider(http_url))

    # Verify connection
    assert client.is_connected(), f"Failed to connect to {http_url}"

    logger.info(f"Web3 client connected to {http_url}")
    return client


@pytest.fixture(scope="session")
def arkiv_client_http(arkiv_node: tuple[DockerContainer | None, str, str]) -> Web3:
    """
    Provide Arkiv client connected to HTTP endpoint.

    Returns:
        Web3 client instance connected to the arkiv node
    """
    _, http_url, _ = arkiv_node
    client = Arkiv(Web3.HTTPProvider(http_url))

    # Verify connection
    assert client.is_connected(), f"Failed to connect Arkiv client to {http_url}"

    logger.info(f"Arkiv client connected to {http_url}")
    return client
