# MLFLow Train Model
This function demonstrates a minimal example of a how to train a cancer classifier ML model using MLFlow framework to structure and represent the model data. The trained model then can be deployed with the MLFlowServe framework or used for batch classifications loading it using the MLFlow framework..

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

The function demonstrates:

Basic syntax of a python script used inside to the platform. It demonstrates
- How to define a function that takes as input 'project' object,  a context in which you can run functions and manage models,data, and artifacts.
- How to fetch input data and train model.
- How to save the trained model in project.

The function 'mlflow-train-model' is registered inside to the platform core durig the import and it can be fetched and executed

```
func = proj.get_function(name="mlflow-train-model") 
```

This code fetch the created function that uses Python runtime (versione 3.10) pointing to the created file and the handler method that should be called. In this case, the code and hanlder is already embedded during the funciton import from the .yaml file.

Then, the function can be executed on the digital hub platform or (locally) as a single job.

Notes: For detailed usage, check the <a href='notebook.ipynb'>usage notebook</a>.


