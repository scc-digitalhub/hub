# LLM OLLAMA Serve

This function demonstrates how to deploy and interact with the LLM model by sending a prompt and receiving a generated response inside the digitalhub platform. The function connects to the Ollama runtime, specifies the llama3.2 model, submits user input, and returns the model’s output, illustrating how applications can integrate local LLM intelligence for secure and efficient AI-powered features.

## Features

The `llm-ollama-serve` function includes the following features:

- **Text Generation**: Generates human-like text based on the provided prompt.
- **Model Customization**: Allows users to specify different models for varied outputs.
- **Real-time Interaction**: Supports real-time requests and responses for dynamic applications.
- **Integration Ready**: Easily integrates with existing applications and workflows.
- **Secure Execution**: Runs within the digitalhub platform for enhanced security.


## Definition

```
llm_OLlama_func = project.new_function(
    name="llm-ollama-serve",
    kind="kubeai-text",
    model_name="llm-ollama-model",
    url="ollama://llama3.2:1b",
    engine='OLlama',
    features=['TextGeneration']
)
```

## Usage

To use the `llm-ollama-serve` function, follow these steps:

1. **Initialize the Project**: Ensure that you have created the project and initialized the function as shown in the definition section.

2. **Start the Serve**: Use the following code to start
 
    ```python
    llm_run = llm_OLlama_func.run("serve", wait=True)
    ```

3. **Invoke the Function**: Use the following code to send a request to the function and receive a response.

    ```python
    import pprint

    model_name =llm_run.refresh().status.k8s.get("Model").get("metadata").get("name")
    json_payload = {'model': CHAT_MODEL, 'prompt': 'Describe MLOps'}
    pp = pprint.PrettyPrinter(indent=2)
    result = llm_run.invoke(json=json_payload, url=service['url']+'/v1/completions').json()
    print("Response:")
    pp.pprint(result)

    ```


Notes: For detailed usage, check the usage notebook.