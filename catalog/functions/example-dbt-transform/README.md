# DBT-Transform
DBT-Transform is a simple DBT transformation operation example that converts the input file (employee table dataitem) to another table using a SQL-based transformation.  Run it with e.g. inputs={"employees": di.key}, and  outputs={"output_table": "department-60"}

## Definition

```
sql = """
WITH tab AS (
    SELECT  *
    FROM    {{ ref('employees') }}
)
SELECT  *
FROM    tab
WHERE   tab."DEPARTMENT_ID" = '50'
"""
```

We define the function:

```python
function = project.new_function(
    name="dbt-transform",
    kind="dbt",
    code=sql
)
```

The parameters are:
    - name is the identifier of the function.
    - kind is the type of the function. Must be dbt.
    - code contains the code that is the SQL we'll execute in the function.

## Fetching the Function

To use an existing DBT transform function, retrieve it from the project context:

```python
function_dbt = proj.get_function("dbt-transform")
```

This fetches the previously defined function by its name, allowing you to execute transformations without redefining the function code.

## Usage

```python
# Run the DBT transform function
run = function_dbt.run(
    "transform",
    inputs={"employees": di.key},
    outputs={"output_table": "department-50"},
    wait=True,
)

# Access the transformed data
df = run.output("department-50").as_df()
```

Notes: For detailed usage, check the usage notebook.
