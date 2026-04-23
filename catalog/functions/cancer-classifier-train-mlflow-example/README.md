# Cancer classifier Training (MLFlow example)

This is a minimal example on how to train a cancer classifier, using the MLFlow framework to structure and represent the model data. The trained model can then be deployed with the MLFlowServe framework, or used for batch classifications with the MLFlow framework.

## Definition

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

The example demonstrates:

- how to define a function that takes as input a `project` object, a context in which you can run functions and manage models, data and artifacts.
- how to fetch input data and train the model.
- how to save the trained model into the project.

The function `mlflow-train-model` is registered inside the platform core during the import and it can be fetched and executed.

```
func = proj.get_function(name="cancer-classifier-train-mlflow-example") 
```

This code fetches the created function that uses Python runtime (version 3.10), pointing to the created file and the handler method that should be called. In this case, code and handler are already embedded during the import from the .yaml file.

Then, the function can be executed on the platform (or locally) as a single job.

For more details, check the notebook.


