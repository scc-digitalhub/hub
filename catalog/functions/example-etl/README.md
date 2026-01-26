# Extract Transform Load Function

This function demonstrates how to create an extract transform load procedure that downloads a CSV file from a remote URL, processes it using pandas, and stores the result as a dataitem in your project. It showcases a basic ETL pattern for ingesting external data sources into your digitalhub project environment.

## Features

- Downloads CSV data from remote URLs
- Processes data using pandas DataFrame operations
- Automatically stores results as dataitems in your project
- Demonstrates basic ETL pattern for data ingestion
- Supports integration with digitalhub runtime environment


## Definition

```python
import pandas as pd
from digitalhub_runtime_python import handler

URL="https://raw.githubusercontent.com/datasets/world-cities/refs/heads/main/data/world-cities.csv"

@handler(outputs=["world-cities"])
def download_and_process():
    df = pd.read_csv(URL)
    df.reset_index(inplace=True)
    return df
```

## Usage

```python
# Create the function
function = project.new_function(
    name="example-etl",
    kind="python",
    source={"source": "example-etl/function.py", "handler": "download_and_process"},
)
```

### Fetching the Function
To use an existing ETL transform function as in this example, retrieve it from the project context.

```python
function = proj.get_function("example-etl")
```

### Run the function
run = function.run("job", wait=True)

### Access the data
dataset_di = proj.get_dataitem("world-cities")
dataset_di.as_df().head()
```

Notes: For detailed usage, check the usage notebook.
