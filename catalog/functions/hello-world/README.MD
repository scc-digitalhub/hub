# Hello world

## Definition


This function demonstrates a minimal example of a function whose sole purpose is to print the classic phrase “Hello, World!” in python. This type of function is traditionally used as an introductory exercise, as it demonstrates the most fundamental structure of a program: outputting text.

## Usage

The function demonstrates:

Basic syntax of a python script used inside to the platform. It demonstrates
- How to define a function
- How to output text to the screen

```
def main(param):
    print(f"Hello {param}")
```

The function 'hello-world' is registered inside to the platform core durig the import and it can be fetched and executed

```
func = proj.get_function(name="hello-world",
                            kind="python",
                            python_version="PYTHON3_10") 
```

This code fetch the created function that uses Python runtime (versione 3.10) pointing to the created file and the handler method that should be called. In this case, the code and hanlder is already embedded during the funciton import from the .yaml file.

Then, the function can be executed on the digital hub platform or (locally) as a single job.

Notes: For detailed usage, check the <a href='usage.ipynb'>usage notebook</a>.


