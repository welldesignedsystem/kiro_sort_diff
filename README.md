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

## Deploy to Streamlit Community Cloud

Streamlit Community Cloud deploys directly from your GitHub repo — no deploy command needed. It watches your branch and redeploys automatically on every push.

### One-time setup

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app**
4. Set:
   - **Repository**: `your-username/your-repo`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Deploy**

After the first deploy, every push to `main` that passes CI will trigger an automatic redeploy.

### CI / CD flow

```
push to main
    └── GitHub Action (ci.yml)
            ├── install deps with uv
            ├── run pytest (skipping perf tests)
            └── verify app imports cleanly
                    └── on success → Streamlit Community Cloud redeploys
```
