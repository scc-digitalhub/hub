# Cancer classfier Serve (MLFlow example)

This function demonstrates how to serve a trained model using Scikit-learn with the DigitalHub SDK. The function will deploy a model as a REST API service.

## Definition
```
serve_func = project.new_function(
    name="serve-classifier",
    kind="sklearnserve",
    path=model.key,
)
```
The `model.key` property represents the unique identifier or path to the trained model artifact in the DigitalHub project. It is used to reference the specific model version that will be deployed for serving.

In this context, `model.key` is passed to the `path` parameter when creating a new serving function, allowing the MLflow-based serving runtime to locate and load the correct model artifact for inference.


## Usage

The function demonstrates:

- **Model serving**: Deploying a trained Scikit-learn model as a REST API endpoint
- **MLflow integration**: Leveraging MLflow's model serving capabilities
- **Inference requests**: Sending prediction requests to the deployed model
- **Resource configuration**: Specifying memory and storage requirements for the service

### Start the service

```
serve_run = serve_func.run("serve", labels=["ml-service"], wait=True)
```

### Send a request
```
import numpy as np

# Generate sample data for prediction
data = np.random.rand(2, 30).tolist()
json_payload = {
    "inputs": [{"name": "input-0", "shape": [2, 30], "datatype": "FP32", "data": data}]
}

# Make prediction
result = serve_run.refresh().invoke(json=json_payload).json()
print("Prediction result:")
print(result)

```

### Response:

```
Prediction result:
{'model_name': 'model', 'id': '40610225-83a3-41e5-86ff-e98873943313', 'parameters': {}, 'outputs': [{'name': 'predict', 'shape': [2, 1], 'datatype': 'INT64', 'parameters': {'content_type': 'np'}, 'data': [1, 1]}]}
```

Notes: For detailed usage, check the usage notebook.