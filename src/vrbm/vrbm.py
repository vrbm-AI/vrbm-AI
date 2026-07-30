import json
import logging
import sys
import urllib.request
import urllib.error
from pathlib import Path
import ast

HEADER_VISIBLE = True
DEFAULT_MODEL = "llama3.1:8b"
TEMPERATURE = 0.7
ALIVE_TIME = "5m"

def load_config():
    global HEADER_VISIBLE, DEFAULT_MODEL, TEMPERATURE

    config = Path("vrbm_config")

    if(not config.exists()):
        return

    for line in config.read_text().splitlines():
        line = line.strip()

        if(not line or line.startswith("#")):
            continue

        key, _, value = line.partition("=")

        key = key.strip().lower()
        value = value.strip()

        if(key == "header_visible"):
            HEADER_VISIBLE = value.lower() == "true"
        elif(key == "model"):
            DEFAULT_MODEL = value
        elif(key == "temperature"):
            TEMPERATURE = float(value)
        elif(key == "alive_time"):
            ALIVE_TIME = value
            
load_config()

logger = logging.getLogger(__name__)

if(HEADER_VISIBLE == True):
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}".rjust(7)
    HEADER = """
        (OvO)
    |--vrbm-AI--|
    |     @     |
    | ver 0.0.1 |
    | py""" + py_version + """ |
    +-----------+
    """ #text content needs to be 9 chars exactly
    
    print(HEADER)

SYSTEM_PROMPT = """You are VRBM Owl (an AI).

Your only job is to output valid Python literals.

Rules:
- Output ONLY the value
- Never explain in any way
- Never use markdown
- Never use code fences
- Never include words before or after the value
- Strings must use double quotes
- Lists must use Python list syntax
- Dictionaries must use Python dictionary syntax
- Tuples must use Python tuple syntax
- If you cannot produce a valid answer that follows all instructions, output only: None

Examples:

User: Give me a random direction. Output type: str
Assistant: "north"

User: Give me three colors. Output type: list
Assistant: ["red","green","blue"]

User: Give me a number. Output type: int
Assistant: 42
"""

VALID_TYPES = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "tuple": tuple,
    "set": set,
    "dict": dict,
    "bytes": bytes,
    "bytearray": bytearray,
    "complex": complex,
}

class VRBMError(Exception):
    pass

class InvalidOutputTypeError(VRBMError):
    pass

class OllamaConnectionError(VRBMError):
    pass

class ModelDownloadError(VRBMError):
    pass

def ollama_chat(model, messages, temp):
    data = {"model": model, "messages": messages, "stream": False, "keep_alive": ALIVE_TIME, "options": {"temperature": temp}}

    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.URLError as e:
        raise OllamaConnectionError("Could not connect to Ollama. Is Ollama running?") from e

def ollama_list():
    request = urllib.request.Request("http://localhost:11434/api/tags")

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.URLError as e:
        raise OllamaConnectionError("Could not connect to Ollama. Is Ollama running?") from e

def ollama_pull(model):
    data = {"name": model, "stream": False}

    request = urllib.request.Request(
        "http://localhost:11434/api/pull",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.URLError as e:
        raise ModelDownloadError(f"Could not download model {model}") from e

def ensure_model(model_name):
    try:
        installed = [model["name"] for model in ollama_list()["models"]]

        if(model_name not in installed):
            logger.info("Model %s not found. Downloading...", model_name)
            ollama_pull(model_name)
            logger.info("Finished downloading %s", model_name)

    except Exception as e:
        raise OllamaConnectionError(f"Could not prepare Ollama model '{model_name}'") from e

def parse_output(output):
    try:
        return ast.literal_eval(output)
    except Exception:
        pass

    try:
        return json.loads(output)
    except Exception:
        pass

    return output

def validate_output(value, expected_type):
    if(expected_type == "unspecified"):
        return None

    expected_class = VALID_TYPES[expected_type]

    if(expected_type == "bool" and type(value) is not bool):
        return f"Expected bool, got {type(value).__name__}"

    if(expected_type != "bool" and not isinstance(value, expected_class)):
        return f"Expected {expected_type}, got {type(value).__name__}"

    return None

def generate(prompt, output_type="unspecified", model=DEFAULT_MODEL, temperature=TEMPERATURE, parse=True):
    ensure_model(model)

    output_type = output_type.lower()

    if(output_type not in VALID_TYPES and output_type != "unspecified"):
        raise InvalidOutputTypeError(f"Invalid output type: {output_type}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": prompt + (f"\nOutput type: {output_type}" if output_type != "unspecified" else "")
        }
    ]

    for attempt in range(3):
        response = ollama_chat(model=model, messages=messages, temp=temperature)

        output = response["message"]["content"].strip()

        if(not parse):
            return output

        value = parse_output(output)
        error = validate_output(value, output_type)

        if(error is None):
            return value

        logger.warning("AI output failed validation (attempt %s/3): %s", attempt + 1, error)

        messages.append({"role": "assistant", "content": output})
        messages.append({
            "role": "user",
            "content": f"Your previous output was invalid.\nProblem: {error}\nTry again. Output only the correct value."
        })

    logger.error("AI failed validation after 3 attempts.")
    return None