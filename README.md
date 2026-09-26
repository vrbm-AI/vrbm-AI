> # vrbm
> > **a python library**

## Setup

1. Run `pip install vrbm-ai` in the terminal
2. Install [Ollama](https://ollama.com)\* for your system (old versions are found [here](https://ollama.en.uptodown.com/windows))
3. Done!

\*This version of `vrbm` (0.0.1) was tested on Ollama version 0.32.5

---

## Why?

I created `vrbm` as a minimal wrapper to use local AI within your Python code. Although it has a very minimal interface, `vrbm` is also very powerful. It supports data type enforcing, smart model downloading, and [more](https://vrbm-AI.github.io/vrbm/). And that's, well, it. 

` (OvO) `

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

A `vrbm_config` file contains the settings for `vrbm` to use at runtime. For more information, go [here](https://vrbm-AI.github.io/vrbm/vrbm_config.html).

---

## Docs

Find the full documentation for vrbm [here](https://vrbm-AI.github.io/vrbm/).

---

### © 2026 vrbm-AI
