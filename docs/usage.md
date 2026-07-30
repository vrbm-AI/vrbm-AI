# Usage Guide

`vrbm‑AI` exposes one main function: `generate()`.

It sends a prompt to Ollama, enforces strict output rules, validates the type, retries on failure, and returns a Python value.

## Basic Example
```python
from vrbm import generate

value = generate("Give me a random color.", output_type="str")
print(value)
```

Output might be:

    "blue"

## Supported Output Types

`vrbm‑AI` can validate:

- str
- int
- float
- bool
- list
- tuple
- set
- dict
- bytes
- bytearray
- complex

Example:

```python
generate("Give me three animals.", output_type="list")
```

## Unspecified Output Type

If you don’t want validation:

```python
generate("Say hello.")
```

## Custom Model

```python
generate("Give me a number.", output_type="int", model="llama3.1:70b")
```

## Disable Parsing

If you want the raw model output:

```python
generate("Give me a number.", parse=False)
```