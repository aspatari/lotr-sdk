#!/bin/bash

# Activate virtual environment if it exists and not already activated
if [ -d ".venv" ] && [ -z "$VIRTUAL_ENV" ]; then
  echo "Activating virtual environment..."
  source .venv/bin/activate
fi

# Check if pytest is installed
if ! command -v pytest >/dev/null 2>&1; then
  echo "Installing development dependencies..."
  uv pip install -e ".[dev]"
fi

# Run the tests
echo "Running unit tests..."
pytest tests/unit/ -v

echo ""
echo "Running integration tests..."
pytest tests/integration/ -v

echo ""
echo "Running tests with coverage..."
pytest --cov=lotr_sdk

echo ""
echo "All tests complete!" 