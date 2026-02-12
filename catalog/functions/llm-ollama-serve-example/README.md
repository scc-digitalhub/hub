# LLM OLLAMA Serve

This function demonstrates how a document classifier model can be operationalizes as a service based on serverless container runtime feature. The service is exposed as an API responding to POST message with the text input and returns the same text back — an echo.

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

### Send a request
```
inputs = {"text": 'trasporto wifi ', "k": 1}
serve_run.invoke(json={"inference_input": inputs}).text
```

### Response:

```
'{"results": [46]}'
```

Notes: For detailed usage, check the usage notebook.