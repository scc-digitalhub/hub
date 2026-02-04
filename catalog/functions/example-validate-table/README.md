# Extract Transform Load Function

This function demonstrates how to validate tabular data using the DigitalHub platform. It performs data quality checks on a table to ensure consistency, completeness, and correctness, generating a comprehensive validation report that includes statistics about errors, warnings, fields, and rows. The function can be used with any table-type data item and provides detailed feedback on the validation status through a JSON report artifact.

## Features

- **Data Quality Validation**: Performs comprehensive checks on tabular data to ensure data integrity
- **Detailed Reporting**: Generates JSON validation reports with error counts, warnings, and field-level statistics
- **Flexible Input**: Works with any table-type data item in the DigitalHub platform
- **Error Detection**: Identifies inconsistencies, missing values, and data quality issues
- **Validation Metrics**: Provides statistics on rows processed, fields validated, and errors encountered


## Definition

```python
import digitalhub as dh
from digitalhub_runtime_python import handler
from frictionless import Checklist, validate
import os

@handler(outputs=["report"])
def main(project, di):
    # download as local file
    path = di.download(overwrite=True)
    # validate
    report = validate(path)
    # update artifact with label    
    label = "VALID" if report.valid else "INVALID"
    di.metadata.labels = di.metadata.labels.append(label) if di.metadata.labels else [label]
    di.save(update=True)    
    #cleanup
    os.remove(path) 

    with open("report.json", "w") as f:
      f.write(report.to_json())

    project.log_artifact(kind="artifact", name=f"{di.name}_validation-report.json", source="report.json")
        
    # persist report
    return report.to_json()
```

## Usage

```python
import digitalhub as dh

# Initialize project
proj = dh.get_or_create_project("my-project")

# Create or get a table data item to validate
di = proj.get_dataitem("my-table")

# Get the validation function
function = proj.get_function("example-validate-table")

# Run validation
run = function.run(action="job", inputs={"di": di.key}, wait=True)

# Retrieve validation report
report = run.output("report")
```
```


### Access the data
report = proj.get_artifact("my-table-report.json")
```

Notes: For detailed usage, check the usage notebook.
