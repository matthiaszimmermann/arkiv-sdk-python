# Golem DB SDK

Golem DB is a permissioned storage system for decentralized apps, supporting flexible entities with binary data, annotations, and metadata.

The Golem DB SDK is the official Python library for interacting with Golem DB networks. It offers a type-safe, developer-friendly API for managing entities, querying data, subscribing to events, and offchain verification—ideal for both rapid prototyping and production use.

## SDK Architecture

### Principles

SDK should be directly derived from one of the most well known and more recent client libraries.

Highlevel goals:
1. Go with the flow of the language and the library.
2. Whatever works for the library should also work for the SDK
3. Feels like "Library + Entities".

### Underlying Libraries

Go per language with modern and battle tested library.

- Javascript/Typescript: [Viem](https://github.com/wevm/viem). Primary choice for most new web3 projects.
- Python: [Web3.py](https://github.com/ethereum/web3.py). No good alternatives.

### Naming

Github "Home": `arkiv-network`
| Language | Element    | Name           | Comment                 |
|----------|------------|----------------|-------------------------|
| Python   | Repository | `arkiv-python` | Golem Base repo: `python-sdk` move and rename to `arkiv-python-beta` |
| TS/JS    | Repository | `arkiv-ts`     | Golem Base repo: `typescript-sdk` move and rename to `arkiv-ts-beta` |
| Python   | PIP        | `pip install arkiv-sdk`   | or `pip install arkiv` as `arkiv` is not available for Rust |
| TS/JS    | NPM        | `npm install arkiv-sdk`   | or `npm install arkiv` as `arkiv` is not available for Rust |


### Arkiv Client (Python)

Goal: Make Arkiv feel like "web3.py + entities", maintaining the familiar developer experience that Python web3 developers.

A `client.entities.*` approach for consistency with web3.py's module pattern. It clearly communicates that arkiv is a module extension just like eth, net, etc.

Here's a comprehensive example showing how to use the Python Arkiv SDK:

```python
from arkiv import Arkiv
from web3 import HTTPProvider

# Initialize Arkiv client (extends Web3)
client = Arkiv(HTTPProvider('https://rpc.arkiv.network'))
client.eth.default_account = '0x742d35cc7731c4532b0b8849d21ca8abeffe5ddd'

# Check connection and balance (standard web3.py functionality)
print(f"Connected: {client.is_connected()}")
balance = client.eth.get_balance(client.eth.default_account)
print(f"Account balance: {client.fromWei(balance, 'ether')} ETH")

# Create entities (Arkiv functionality)
print("\n=== Creating Entities ===")

# Simple entity with data only
entity_key1 = client.arkiv.create_entity(
    data=b"Hello, Arkiv!",
    annotations={"type": "greeting", "version": 1}
)
print(f"Created entity 1: {entity_key1}")

# Get individual entity
print("\n=== Entity Details ===")
entity = client.arkiv.get_entity(entity_key1)
print(f"Entity data: {entity.entity.data.decode()}")
print(f"Entity annotations: {entity.entity.annotations}")
print(f"Entity owner: {entity.entity.metadata.owner}")
print(f"Entity version: {entity.entity.metadata.version}")

# Clean up - delete entities
print("\n=== Cleanup ===")
client.arkiv.delete_entity(entity_key1)
client.arkiv.delete_entity(entity_key2)
print("Entities deleted")

# Verify deletion
exists = client.arkiv.exists_entity(entity_key1)
print(f"Entity 1 still exists: {exists.exists}")
```


#### Javascript Arkiv Client

Goal: Make Arkiv feel like "viem + entities" rather than a separate library.

```typescript
import { createArkivPublicClient, createArkivWalletClient } from 'arkiv'
import { http } from 'viem'
import { arkivMainnet } from 'arkiv/chains'

const publicClient = createArkivPublicClient({
  chain: arkivMainnet,
  transport: http('https://rpc.arkiv.network')
})

const walletClient = createArkivWalletClient({
  chain: arkivMainnet,
  transport: http('https://rpc.arkiv.network'),
  account: privateKeyToAccount('0x...')
})

// Standard blockchain operations
const balance = await publicClient.getBalance({
  address: '0x...'
})

// Write operations
const txHash = await walletClient.createEntity({
  data: new Uint8Array([1, 2, 3, 4]),
  annotations: { purpose: 'demo' }
})
```

# Development Guide

## Code Quality and Type Safety

This project uses comprehensive linting and type checking to maintain high code quality:

### Tools Used

- **MyPy**: Static type checker with strict configuration
- **Ruff**: Fast linter and formatter (replaces black, isort, flake8, etc.)
- **Pre-commit**: Automated quality checks on git commits

### Quick Commands

```bash
# Run all quality checks
./scripts/check-all.sh

# Individual tools
uv run ruff check . --fix    # Lint and auto-fix
uv run ruff format .         # Format code
uv run mypy src/ tests/      # Type check
uv run pytest tests/ -v     # Run tests
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit` and will:
- Fix linting issues with ruff
- Format code consistently
- Run type checking with mypy
- Check file formatting (trailing whitespace, etc.)

To run pre-commit manually:
```bash
uv run pre-commit run --all-files
```

### Type Hints Best Practices

1. **Always use type hints** for function parameters and return values
2. **Use specific types** instead of `Any` when possible
3. **Import types** from `typing` or `collections.abc` as needed
4. **Use Union types** for multiple acceptable types: `str | int`
5. **Generic containers**: `list[str]`, `dict[str, int]`, etc.

### Example Type-Safe Code

```python
from collections.abc import Generator
from typing import Any

def process_data(items: list[dict[str, Any]]) -> Generator[str, None, None]:
    """Process data items and yield formatted strings."""
    for item in items:
        if isinstance(item.get("name"), str):
            yield f"Processing: {item['name']}"
```

### MyPy Configuration

The project uses strict mypy settings:
- `strict = true` - Enable all strict checks
- `no_implicit_reexport = true` - Require explicit re-exports
- `warn_return_any = true` - Warn about returning Any values
- Missing imports are ignored for third-party libraries without type stubs

### Ruff Configuration

Ruff is configured to:
- Use 88 character line length (Black-compatible)
- Target Python 3.12+ features
- Enable comprehensive rule sets (pycodestyle, pyflakes, isort, etc.)
- Auto-fix issues where possible
- Format with double quotes and trailing commas
