# Cancer Classifier Service

This project implements a cancer classification service that trains and deploys a machine learning model to categorize cancer data. It enables users to classify cancer samples using a fine-tuned SVM model with MLflow integration. The service supports both training and inference workflows on the platform.

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

A Python batch-processing function that trains a cancer classification model.

**Key specifications:**

- Python version: 3.10
- Handler: Model training using SVM with GridSearchCV
- Primary dependencies: MLflow, Scikit-learn
- Purpose: Trains an SVM classifier on cancer datasets with automatic logging

```
import pandas as pd
from sklearn.datasets import load_breast_cancer

from digitalhub_runtime_python import handler

from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from pickle import dump
import sklearn.metrics
import os

@handler()
def breast_cancer_generator(project):
    """
    A function which generates the breast cancer dataset
    """
    breast_cancer = load_breast_cancer()
    df_cancer = pd.DataFrame(
        data=breast_cancer.data, columns=breast_cancer.feature_names
    )
    breast_cancer_labels = pd.DataFrame(data=breast_cancer.target, columns=["target"])
    df_cancer = pd.concat(
        [df_cancer, breast_cancer_labels], axis=1
    )

    X = df_cancer.drop(['target'],axis=1)
    y = df_cancer['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=5)
    svc_model = SVC()
    svc_model.fit(X_train, y_train)
    y_predict = svc_model.predict(X_test)

    if not os.path.exists("model"):
        os.makedirs("model")

    with open("model/cancer_classifier.pkl", "wb") as f:
        dump(svc_model, f, protocol=5)

    metrics = {
        "f1_score": sklearn.metrics.f1_score(y_test, y_predict),
        "accuracy": sklearn.metrics.accuracy_score(y_test, y_predict),
        "precision": sklearn.metrics.precision_score(y_test, y_predict),
        "recall": sklearn.metrics.recall_score(y_test, y_predict),
    }
    project.log_model(
            name="cancer_classifier",
            kind="sklearn",
            source="./model/",
            metrics=metrics
    )
```

## Usage

The function demonstrates:

- how to define a function that takes as input a `project` object, a context in which you can run functions and manage models, data and artifacts.
- How to fetch input data and train model.
- How to save the trained model in project.

The `cancer-classifier-train` function is registered inside the platform core during the import and it can be fetched and executed.

```
func = proj.get_function(name="cancer-classifier-train") 
```

This code fetches the created function that uses Python runtime (version 3.10), pointing to the created file and the handler method that should be called. In this case, code and handler are already embedded during the import from the .yaml file.

Then, the function can be executed on the platform (or locally) as a single job.

### cancer-classifier-serve

This function demonstrates how to serve a trained model using Scikit-learn with the platform's SDK. The function will deploy a model as a REST API service.

## Definition

```
serve_func = project.new_function(
    name="serve-classifier",
    kind="sklearnserve",
    path=model.key,
)
```

The `model.key` property represents the unique identifier or path to the trained model artifact in the project. It is used to reference the specific model version that will be deployed for serving.

In this context, `model.key` is passed to the `path` parameter when creating a new serving function, allowing the MLflow-based serving runtime to locate and load the correct model artifact for inference.

```
model = project.get_model("cancer_classifier")
```

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

For more details, check the notebook.