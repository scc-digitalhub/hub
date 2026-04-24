# Hello world
This function demonstrates a minimal example of a function to print the classic phrase *“Hello, World!”* in python.

## Definition

```
def main(param):
    print(f"Hello {param}")
```

## Usage

The function demonstrates:

- How to define a function that takes a parameter
- How to print a *Hello {parameter}* message

The `hello-world` function is registered into the platform core during the import and it can be fetched and executed:

```
func = proj.get_function(name="hello-world",
                            kind="python",
                            python_version="PYTHON3_10") 
```

This code fetches the created function with Python runtime (version 3.10), pointing to the created file and the handler method that should be called. In this case, the code and handler are already embedded during the import from the .yaml file.

Then, the function can be executed on the platform (or locally) as a single job.

For detailed usage, check the notebook.


