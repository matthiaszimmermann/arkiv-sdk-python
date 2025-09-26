# Dependency Groups Usage Examples

The streamlined dependency structure allows for more targeted installation:

## **🧪 Testing Only**
```bash
uv sync --group test
# Installs: pytest, testcontainers, websockets
# Use case: CI/CD testing pipelines
```

## **🔍 Linting Only**
```bash
uv sync --group lint
# Installs: mypy, ruff, pre-commit
# Use case: Code quality checks, static analysis
```

## **⚙️ Development Utilities**
```bash
uv sync --group dev
# Installs: python-dotenv
# Use case: Local development configuration
```

## **🎯 Full Development Environment**
```bash
uv sync --group test --group lint --group dev
# Installs all development dependencies
# Use case: Complete local development setup
```

## **🚀 Benefits**

### **Faster CI/CD**
- Test runners can install only `--group test`
- Linting jobs can install only `--group lint`
- Reduces installation time and image size

### **Clearer Organization**
- Dependencies grouped by purpose
- Easy to understand what each group provides
- Better documentation and maintenance

### **Selective Development**
- Developers can choose what they need
- Lighter installations for specific tasks
- Better separation of concerns
