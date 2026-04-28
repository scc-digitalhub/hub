# Cancer classifier Training (MLFlow example)

This is a minimal example on how to train a cancer classifier, using the MLFlow framework to structure and represent the model data. The trained model can then be deployed with the MLFlowServe framework, or used for batch classifications with the MLFlow framework.

## Definition

```
from digitalhub_runtime_python import handler
from urllib.parse import urlparse
import mlflow
from sklearn import datasets, svm
from sklearn.model_selection import GridSearchCV

@handler(outputs=["model"])
def train(project):
    mlflow.sklearn.autolog(log_datasets=True)

    iris = datasets.load_iris()
    parameters = {"kernel": ("linear", "rbf"), "C": [1, 10]}
    svc = svm.SVC()
    clf = GridSearchCV(svc, parameters)

    clf.fit(iris.data, iris.target)
    run_id = mlflow.last_active_run().info.run_id

    # Extract MLflow run artifacts and metadata for platform integration
    model_params, metrics = _from_mlflow_run(run_id)
    
    model = project.log_model(name="model-mlflow", kind="mlflow", **model_params)
    

    project.log_model(
        name="model-mlflow",
        kind="mlflow",
        **model_params)
        
    model.log_metrics(metrics)
    
    return model    



def _from_mlflow_run(run_id: str) -> dict:
    """
    Extract from mlflow run spec for platform Model.

    Parameters
    ----------
    run_id : str
        The id of the mlflow run.

    Returns
    -------
    dict
        The extracted spec.
    """

    # Get MLFlow run
    run = mlflow.MlflowClient().get_run(run_id)

    # Extract spec
    data = run.data
    parameters = data.params
    source_path = urlparse(run.info.artifact_uri).path + "/model"
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.pyfunc.load_model(model_uri=model_uri)
    try:
        model_config = model.model_config
    except Exception:
        model_config = {}
    flavor = None
    for f in model.metadata.flavors:
        if f != "python_function":
            flavor = f
            break

    # Extract signature
    try:
        mlflow_signature = model.metadata.signature
        signature = dict(
            inputs=mlflow_signature.inputs.to_json()
            if mlflow_signature.inputs
            else None,
            outputs=mlflow_signature.outputs.to_json()
            if mlflow_signature.outputs
            else None,
            params=mlflow_signature.params.to_json()
            if mlflow_signature.params
            else None,
        )
    except Exception:
        signature = None

    # Extract datasets
    datasets = []
    try:
        if run.inputs and run.inputs.dataset_inputs:
            datasets = [
                dict(
                    name=d.dataset.name,
                    digest=d.dataset.digest,
                    profile=d.dataset.profile,
                    dataset_schema=d.dataset.schema,
                    source=d.dataset.source,
                    source_type=d.dataset.source_type,
                )
                for d in run.inputs.dataset_inputs
            ]
    except Exception:
        datasets = []

    # Create model params
    model_params = {}

    # source path
    model_params["source"] = source_path

    # common properties
    model_params["framework"] = flavor
    model_params["parameters"] = parameters

    # specific to MLFlow
    model_params["flavor"] = flavor
    model_params["model_config"] = model_config
    model_params["input_datasets"] = datasets
    model_params["signature"] = signature

    metrics = run.data.metrics

    return model_params, metrics
    
```

## Usage

The example demonstrates:

- how to define a function that takes as input a `project` object, a context in which you can run functions and manage models, data and artifacts.
- how to fetch input data and train the model.
- how to save the trained model into the project.

The `mlflow-train-model` function is registered inside the platform core during the import and it can be fetched and executed.

```
func = proj.get_function(name="cancer-classifier-train-mlflow-example") 
```

This code fetches the created function that uses Python runtime (version 3.10), pointing to the created file and the handler method that should be called. In this case, code and handler are already embedded during the import from the .yaml file.

Then, the function can be executed on the platform (or locally) as a single job.

For more details, check the notebook.


