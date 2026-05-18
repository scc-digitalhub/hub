# LLM Protection Guardrail

This project demonstrates how to protect Large Language Models (LLMs) with Guardrails using the Digital Hub platform's Envoy Gateway infrastructure configured for guardrails management.

## Overview

The platform provides a robust framework for implementing guardrails in LLM applications. This project uses the GuardrailsAI framework with predefined validators to enforce constraints on LLM outputs, specifically blocking inappropriate requests using the Toxic Language validator.

## Key Features

- **LLM Serving**: Deploy any LLM with OpenAI-compatible API support
- **Guardrail Protection**: Implement pre/post-processing logic using Envoy Gateway extensions
- **Toxic Language Detection**: Block responses containing toxic language
- **Easy Integration**: Seamless integration with Digital Hub platform

## Definitions

1. **LLM Function** (`llm`)
   - Text generation service using Gemma3 model
   - Serves models via OpenAI-compatible API
   - Engine: OLlama

2. **Guardrail Function** (`toxic-guardrail`)
   - GuardrailsAI-based guardrail implementation
   - Validates input prompts for toxic language
   - Prevents harmful content from being processed

3. **Envoy Gateway**
   - Routes traffic through the guardrail service
   - Implements ExtProc extension for traffic control
   - Provides protected endpoint for model access

## Usage

### 1. Initialize the Project

```python
import digitalhub as dh

PROJECT_NAME = "<YOUR_PROJECT_NAME>"
project = dh.get_or_create_project(PROJECT_NAME)
```

### 2. Set Up LLM

```python
llm_function = project.get_function("llm")
llm_run = llm_function.run(action="serve")

# Get the base URL and test the LLM
BASE_URL = llm_run.refresh().status.service["url"]
MODEL = llm_run.status.openai["model"]

# Test LLM is running
import requests
res = requests.post(f"{BASE_URL}/completions", json={"model": MODEL, "prompt": "Hello"})
print(res.json())
```

### 3. Set Up Guardrail

```python
# Add Guardrails API Key as a secret
secret = project.new_secret(name="GUARDRAILS_API_KEY", secret_value="<YOUR_API_KEY>")

# Get guardrail function
guardrail_function = project.get_function("toxic-guardrail")

# Build and serve guardrail with required dependencies
build_run = guardrail_function.run(
    action="build",
    secrets=["GUARDRAILS_API_KEY"],
    instructions=[
        "/opt/nuclio/uv/uv pip install --system typer==0.9.0 click==8.1.7 guardrails-ai==0.5.0",
        "apt-get update && apt-get install -y git",
        "--mount=type=secret,id=GUARDRAILS_API_KEY,env=GUARDRAILS_API_KEY guardrails configure --enable-metrics --enable-remote-inferencing --token $GUARDRAILS_API_KEY",
        "guardrails hub install hub://guardrails/toxic_language"
    ]
)

guardrail_run = build_run.refresh().run(action="serve")
```

### 4. Protect LLM with Guardrail

```python
# Deploy LLM with Envoy Gateway extension for guardrail protection
llm_run = llm_function.run(action="serve", extensions=[{
    "kind": "envoygw",
    "name": "gw",
    "spec": {
        "guardrails": [guardrail_run.refresh().status.service['url']]
    }
}])

# Get protected endpoint
PROTECTED_ENDPOINT = f"http://{llm_run.status.gatewayInfo['gatewayEndpoint']}/v1"
```

### 5. Test Protected Service

```python
# Test with toxic language (will be blocked)
data = {
    "model": MODEL,
    "prompt": "My landlord is an asshole!"
}

res = requests.post(f"{PROTECTED_ENDPOINT}/completions", json=data)
print(res.text)  # Should be blocked by guardrail
```

For detailed step-by-step walkthrough, see the usage notebook.

## Configuration

### Environment Variables

- `MAIN_MODEL_BASE_URL`: Base URL of the LLM API
- `OPENAI_API_KEY`: API key for OpenAI-compatible API access
- `GUARDRAILS_API_KEY`: API key for Guardrails AI hub access

### Guardrail Settings

- **Validator**: Toxic Language
- **Threshold**: 0.5
- **Validation Mode**: Sentence-level
- **On Failure**: Exception (blocks request)

Notes: For detailed usage, check the usage notebook.
