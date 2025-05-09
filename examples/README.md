# LOTR SDK Usage Examples

This directory contains examples demonstrating how to use the LOTR SDK in both synchronous and asynchronous modes.

## Examples Overview

1. **Synchronous Example** (`sync_example.py`): Shows how to use the SDK with blocking calls
2. **Asynchronous Example** (`async_example.py`): Shows how to use the SDK with non-blocking calls for better performance

Both examples perform the same task:
- Fetch all Lord of the Rings movies
- For each movie, retrieve all of its quotes
- Count quotes containing numeric characters
- Display statistics about quotes per movie

The examples are designed to demonstrate the performance difference between synchronous and asynchronous approaches.

## Installation and Setup

### 1. Install uv

First, install `uv` following the [official documentation](https://docs.astral.sh/uv/getting-started/installation/):

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```bash
git clone https://github.com/aspatari/lotr-sdk.git
cd lotr-sdk
```

### 3. Create a Python 3.13 virtual environment

```bash
# Create a Python 3.13 environment
uv venv -p 3.13

# Activate the environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 4. Install dependencies

```bash
# Install the SDK and its dependencies
uv sync
```

The examples already include a sample API key (`qQg8z34W2l1bV1I1jGr_`).

## Running the Examples

Make sure your virtual environment is activated, then run:

### 1. Synchronous example

```bash
uv run examples/sync_example.py
```

### 2. Asynchronous example

```bash
uv run examples/async_example.py
```

### 3. Compare the results

After running both examples, compare the execution times displayed at the end of each run:

```
# Example output - Synchronous version
⏱️ Total execution time: 3.15 seconds

# Example output - Asynchronous version
⏱️ Total execution time: 2.16 seconds
```

The asynchronous version runs significantly faster because it fetches quotes for different movies concurrently.

## Results

Both examples will produce similar output, showing:
- A list of movies and their quotes
- The number of quotes containing numeric characters per movie
- A sorted list of movies by the number of quotes containing numbers
- The total execution time

The key difference is in performance:
- **Synchronous**: ~3.15 seconds for processing all movies sequentially
- **Asynchronous**: ~2.16 seconds for processing all movies concurrently

This performance improvement would be even more significant with more movies or when dealing with slower networks.

## Notes on Python Version

This SDK requires Python 3.13 or later. Make sure you're using the correct Python version when creating your virtual environment.

## Notes on Performance

- The asynchronous example is faster because it processes all movies concurrently.
- For small datasets, the difference might be minimal, but it becomes significant with larger datasets.
- The bottleneck in these examples is primarily network I/O, which is exactly where async processing shines. 