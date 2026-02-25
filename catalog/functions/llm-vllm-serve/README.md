# VLLM Serve

This function deploys a large language model (LLM) using the VLLM engine within the digitalhub platform. It provides an OpenAI-compatible API endpoint for text generation tasks. Users can submit prompts to the deployed model and receive generated completions in real-time. The deployment is containerized and runs on Kubernetes, supporting various optimization options such as dtype specification and resource profiles for efficient inference.


## Features

The `llm-vllm-serve` function includes the following features:

- **OpenAI-compatible API**: Provides a REST API endpoint compatible with OpenAI's text completion format
- **Multiple model support**: Deploy various open-source LLMs from Hugging Face Hub
- **Performance optimization**: Configurable dtype (float16, float32) and quantization options
- **Resource flexibility**: Support for different GPU profiles (1xV100, 2xA100, etc.) based on deployment needs
- **Real-time inference**: Stream generated text completions as they are produced
- **Kubernetes-native**: Containerized deployment with automatic scaling and health monitoring
- **Batch processing**: Handle single and batched requests efficiently


## Definition

The `llm-vllm-serve` function supports the following configuration options:

- **Model Selection**: Specify any model from Hugging Face Hub using the `url` parameter (format: `hf://model-name`)
- **Data Type (dtype)**: Choose between `float16`, `float32`, or `bfloat16` for model precision and memory optimization
- **Quantization**: Enable quantization methods like AWQ or GPTQ for reduced memory footprint
- **GPU Profiles**: Select appropriate GPU resources (`1xV100`, `2xA100`, `1xL40S`, etc.)
- **Tensor Parallelism**: Distribute model inference across multiple GPUs
- **Max Tokens**: Configure maximum generation length per request
- **Temperature & Sampling**: Control output randomness and decoding strategy
- **Batch Size**: Tune concurrent request handling
- **API Port**: Customize the service endpoint port configuration

```
llm_vllm_func = project.new_function(
    name="llm-vllm-serve",
    kind="kubeai-text",
    model_name="model",
    url="hf://Qwen/Qwen2.5-0.5B-Instruct",
    engine='VLLM',
    features=['TextGeneration']
)
```

## Usage

To use the `llm-vllm-serve` function, follow these steps:

1. **Initialize the Project**: Ensure that you have created the project and initialized the function as shown in the definition section.

2. **Start the Serve**: Use the following code to start. 
 
    ```python
    vllm_run = llm_vllm_func.run("serve", profile="1xV100", args=["--dtype=float16"], wait=True)
    ```

3. **Invoke the Function**: Use the following code to send a request to the function and receive a response.

    ```python
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    result = vllm_run.invoke(json=json_payload, url=service['url']+'/v1/completions').json()
    print("Response:")
    pp.pprint(result)
    ```


Notes: For detailed usage, check the usage notebook.

## Resources

These settings define the resource requests and limits for the runtime.

| Resource | Value | Description |
| -------- | ----- | ----------- |
| **GPU Type** | `V100` or `A100` | GPU accelerator for model inference. |


The `llm-vllm-serve` function requires GPU acceleration to operationalize large language models efficiently. GPU is mandatory for model inference and cannot be replaced by CPU-only computation.
