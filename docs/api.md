# API Reference

This page documents all public functions, classes, and behaviors in VRBM‑AI.

# Global Settings

- `HEADER_VISIBLE`
- `DEFAULT_MODEL`
- `TEMPERATURE`
- `ALIVE_TIME`

Loaded from `vrbm_config` if present.

# Exceptions

### `VRBMError`
Base class for all `vrbm‑AI` errors.

### `InvalidOutputTypeError`
Raised when the user requests an unsupported output type.

### `OllamaConnectionError`
Raised when `vrbm‑AI` cannot reach the Ollama server.

### `ModelDownloadError`
Raised when a model cannot be downloaded.

# Functions*
### *only `generate()` is exposed

## `load_config()`
Reads the `vrbm_config` file and updates global settings.

## `ollama_chat(model, messages, temp)`
Low‑level wrapper around Ollama’s `/api/chat`.
Returns the raw `JSON` response.

## `ollama_list()`
Returns a list of installed Ollama models.

## `ollama_pull(model)`
Downloads a model if not installed.

## `ensure_model(model_name)`
Checks if a model exists; downloads it if missing.

## `parse_output(output)`
Attempts to parse model output using:
1. `ast.literal_eval`
2. `json.loads`
3. `raw string fallback`

## `validate_output(value, expected_type)`
Ensures the returned value matches the requested type.
Returns:
- `None` if valid
- error message string if invalid

## `generate(prompt, output_type="unspecified", model=DEFAULT_MODEL, temperature=TEMPERATURE, parse=True)`
Main user‑facing function.

### Behavior:
1. Ensures model is installed
2. Sends system + user messages
3. Parses output
4. Validates type
5. Retries up to 3 times
6. Returns Python value or `None`

### Parameters:
- `prompt`: user text
- `output_type`: Python type name
- `model`: Ollama model
- `temperature`: float
- `parse`: whether to parse output

### Returns:
- Python value
- or `None` on failure

# Constants

## `SYSTEM_PROMPT`
Strict instructions sent to Ollama to enforce Python literal output.

## `VALID_TYPES`
Mapping of type names → Python classes.

---

[< prev.](vrbm_config.md) | [home](index.md)