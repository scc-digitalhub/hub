# Cancer Classifier Service

This project implements a cancer classification service that trains and deploys a machine learning model to categorize cancer data. It enables users to classify cancer samples using a fine-tuned SVM model with MLflow integration. The service supports both training and inference workflows on the DigitalHub platform.

## Features

The `cancer-classifier-service` includes the following features:

- **Model training**: Train SVM-based cancer classification models using MLflow framework
- **Hyperparameter tuning**: Grid search optimization for kernel and regularization parameters
- **MLflow integration**: Automatic logging of model artifacts and parameters
- **REST API inference**: Deploy trained models as REST endpoints for predictions
- **Model versioning**: Trained models are automatically logged and versioned on the platform
- **Scikit-learn compatibility**: Native support for sklearn models with MLflowServe runtime
- **Batch classification**: Load and use models for batch predictions

## Definition

### cancer-classifier-train

A Python batch processing function that trains a cancer classification model.

**Key specifications:**

- Python version: 3.10
- Handler: Model training using SVM with GridSearchCV
- Primary dependencies: MLflow, Scikit-learn
- Purpose: Trains an SVM classifier on cancer datasets with automatic logging

```
from digitalhub_runtime_python import handler

from digitalhub import from_mlflow_run
import mlflow

from sklearn import datasets, svm
from sklearn.model_selection import GridSearchCV

@handler()
def train(project):
    mlflow.sklearn.autolog(log_datasets=True)

    iris = datasets.load_iris()
    parameters = {"kernel": ("linear", "rbf"), "C": [1, 10]}
    svc = svm.SVC()
    clf = GridSearchCV(svc, parameters)

    clf.fit(iris.data, iris.target)
    run_id = mlflow.last_active_run().info.run_id

    # utility to map mlflow run artifacts to model metadata
    model_params = from_mlflow_run(run_id)

    project.log_model(
        name="model-mlflow",
        kind="mlflow",
        **model_params
```

## Usage

The function demonstrates:

Basic syntax of a python script used inside to the platform. It demonstrates

- How to define a function that takes as input 'project' object,  a context in which you can run functions and manage models,data, and artifacts.
- How to fetch input data and train model.
- How to save the trained model in project.

The function 'cancer-classifier-train' is registered inside to the platform core durig the import and it can be fetched and executed

```
func = proj.get_function(name="cancer-classifier-train") 
```

This code fetch the created function that uses Python runtime (versione 3.10) pointing to the created file and the handler method that should be called. In this case, the code and hanlder is already embedded during the funciton import from the .yaml file.

Then, the function can be executed on the digital hub platform or (locally) as a single job.

Notes: For detailed usage, check the usage notebook.


### cancer-classifier-serve

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