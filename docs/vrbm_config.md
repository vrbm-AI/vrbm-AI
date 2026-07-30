# Configuration File: `vrbm_config`

`vrbm‑AI` reads a simple configuration file named `vrbm_config` located in the same folder as your project.

Example file:

    header_visible=true
    model=llama3.1:8b
    temperature=0.7
    alive_time=5m

## Available Settings

### `header_visible`
Whether the ASCII owl header prints on startup.

Values:
- `true`
- `false`

### `model`
Default Ollama model to use.

Example:
`model=llama3.1:8b`

### `temperature`
Floating‑point temperature value.

Example:
`temperature=0.5`

### `alive_time`
How long Ollama keeps the model warm.

Example:
`alive_time=5m`

## Behavior

If `vrbm_config` does not exist, `vrbm‑AI` uses built‑in defaults:

- `header_visible = true`
- `model = "llama3.1:8b"`
- `temperature = 0.7`
- `alive_time = "5m"`

---

[< prev.](usage.md) | [home](index.md) | [next >](api.md)