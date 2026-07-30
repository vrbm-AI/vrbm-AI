> # vrbm-AI
> > **a python library**

## Setup

1. Run `pip install vrbm-ai` in the terminal
2. Install [Ollama](https://ollama.com)\* for your system (old versions are found [here](https://ollama.en.uptodown.com/windows))
3. Done!

\*This version of `vrbm-ai` (0.0.1) was tested on Ollama version 0.32.5

---

## How to Use

### Example Code

`test.py`
```python
from vrbm import *

prompt = "Make a list of 9 random values."

result = generate(prompt, "list")
print(result)
```

`vrbm_config`
```
header_visible=true
model=llama3.1:8b
temperature=0.7
alive_time=5m
```

### What is a `vrbm_config` file?

A `vrbm_config` file contains the settings for `vrbm-ai` to use at runtime. For more information, go [here](https://vrbm-AI.github.io/vrbm-AI/vrbm_config/).

---

## Docs

Find the full documentation for vrbm-AI [here](https://vrbm-AI.github.io/vrbm-AI/).

---

### © 2026 vrbm-AI