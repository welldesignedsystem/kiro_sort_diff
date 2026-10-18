# String Sort Visualizer

A Streamlit app that sorts strings using Bubble Sort, Selection Sort, and Quick Sort — showing the sorted output, comparison step count, and accuracy check for each algorithm side by side.

## Setup

Uses [uv](https://github.com/astral-sh/uv) for environment management.

```bash
# Create the virtual environment
uv venv .venv

# Install dependencies
uv pip install -r requirements.txt
```

## Run

```bash
uv run streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Usage

1. **Enter strings manually** — type one string per line in the text area, or
2. **Pick from the word list** — select words from the multiselect dropdown
3. Click **Sort** to run all three algorithms
4. Results appear side by side with step counts and accuracy indicators

## Run Tests

```bash
uv run pytest
```

To skip the performance test:

```bash
uv run pytest -m "not perf"
```
