
# LLM Nemo Guardrail

A guardrail system for Large Language Models using Apache Tika and NeMo Guardrails to ensure safe and appropriate content handling. This project provides:

- **Content Safety**: NeMo Guardrails proxy service to filter harmful content
- **LLM Serving**: Gemma3 model served via Ollama with OpenAI-compatible APIs


## Features

- **Real-time Content Filtering**: Intercept and filter LLM responses using NeMo Guardrails policies
- **Multi-model Support**: Compatible with any OpenAI-compatible LLM endpoint
- **Easy Deployment**: Kubernetes-native deployment with DigitalHub
- **Configurable Guardrails**: Customize safety policies and guardrail configurations
- **High Performance**: Proxy service with minimal latency overhead


## Definitions

### `llm`
Serves the Gemma3 model via Ollama with OpenAI-compatible APIs for LLM inference.

### `nemo-guardrail`
NeMo Guardrails proxy service that intercepts and filters LLM responses based on configured safety policies.


## Usage

### 1. Initialize the Project

```python
import digitalhub as dh
PROJECT_NAME = "<YOUR_PROJECT_NAME>"
project = dh.get_or_create_project(PROJECT_NAME)
```

### 2. Deploy the LLM

```python
llm_function = project.get_function("llm")
llm_run = llm_function.run(action="serve")
```

### 3. Deploy NeMo Guardrails

```python
guardrail_function = project.get_function("nemo-guardrail")
guardrail_run = guardrail_function.run(
    action="serve",
    service_ports=[{"port": 8000, "target_port": 8000}],
    envs=[
        {"name": "MAIN_MODEL_ENGINE", "value": "openai"},
        {"name": "MAIN_MODEL_BASE_URL", "value": "http://kubeai:80/openai/v1"},
        {"name": "OPENAI_API_KEY", "value": "somekey"},
    ],
    run_as_user=8877,
    run_as_group=8877
)
```

### 4. Use the Guardrailed LLM

```python
data = {
    "model": MODEL,
    "messages": [{"role": "user", "content": "Your prompt here"}],
    "guardrails": {"config_id": "hello_world"}
}

res = requests.post(f"{GUARDRAIL_URL}/v1/chat/completions", json=data)
```

Notes: For detailed usage, check the usage notebook.


