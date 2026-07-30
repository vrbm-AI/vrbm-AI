# Installation

`vrbm‑AI` requires:

- Python 3.8+
- Ollama installed and running locally
- Storage space for at least one Ollama model (default: llama3.1:8b)

## Install `vrbm‑AI`

Run:

    pip install vrbm-ai

Or install locally in editable mode:

    pip install -e .

## Install Ollama

Download Ollama (recommended version `0.32.5`) from:

    https://ollama.com

Make sure the Ollama server is running at [`http://localhost:11434/`](http://localhost:11434/).

## Verify installation

Example:

```python
from vrbm import generate
print(generate("Give me a number.", output_type="int"))
```

If you see a valid integer, everything is working.