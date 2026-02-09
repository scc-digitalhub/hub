# Container Function

The DigitalHub Platform  Container runtime enables launching services on Kubernetes. It registers function kind 'container' and supports various actions for containerized workloads including jobs, services and builds. This function demonstrates how to serve a 'job' that can be run in a containerized environment using predefined base images. The function act as a template for serving custom container within the platform. As a general confromance to best practice approach, the container runtime is executed as non root user(fs_group='8877')


## Features

- **Kubernetes-based deployment**: Run containerized workloads on Kubernetes infrastructure
- **Service hosting**: Deploy and serve applications using the `serve` action
- **Customizable configuration**: Configure replicas, service ports, and service names
- **Security-first**: Runs as non-root user (fs_group='8877') following best practices
- **Pre-built image support**: Use existing container images like `hashicorp/http-echo`
- **Flexible port mapping**: Configure both internal and external port mappings for network access


## Definition
```python
import digitalhub as dh

# Initialize project
proj = dh.get_or_create_project("my-project")

# Create function
function = project.new_function(
    kind="container",
    name="my_container_function_serve",
    image="hashicorp/http-echo:latest",
)
```

## Usage


The `serve` action starts a web server to host and serve your application or content. It accepts parameters to configure the deployment including the number of replicas, service ports for network access, a custom service name. The `port` is the external port exposed by the Kubernetes service for external access for incoming traffic to service, while `target_port` is the internal port where the container application is listening for requests i.e port numer where traffic routed to pod.

```python
# Run the container function as a job
run = function.run(
    action="serve",
    replicas=2,
    service_ports=[{"port": 5678, "target_port": 5678}],
    service_name="http-echo",
    run_as_user="8877",
    wait=True,
)
```

Notes: For detailed usage, check the usage notebook.