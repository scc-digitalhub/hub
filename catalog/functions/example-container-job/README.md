# Container Function

The DigitalHub Platform  Container runtime enables launching pods, jobs and services on Kubernetes. It registers Function kind container and supports various actions for containerized workloads including jobs, services and builds. This function demonstrates how to create a Python job that can be run in a containerized environment using predefined base images. This function serves as a template for building custom container jobs within the platform. As a general confromance to best practice approach, the container runtime is executed as non root user(fs_group='8877')


## Features

- **Container-based execution**: Run jobs in isolated containerized environments
- **Kubernetes integration**: Seamlessly execute workloads on Kubernetes clusters
- **Flexible runtime**: Support for custom Docker images and base images
- **Job management**: Track and monitor containerized job execution
- **Scalable processing**: Leverage Kubernetes for distributed workload execution


## Definition
```python
import digitalhub as dh

# Initialize project
proj = dh.get_or_create_project("my-project")

# Create function
function = proj.new_function(
    kind="container",
    name="my_container_function_job",
    image="hello-world:latest",
)
```

## Usage

```python
# Run the container function as a job
run = function.run(
    action="job",
    run_as_user="8877",
    wait=True,
)
```

Notes: For detailed usage, check the usage notebook.