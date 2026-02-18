# Flower Serve

The `flower-serve` function provides a scalable federated learning server implementation using the Flower framework. It enables distributed machine learning where multiple client nodes perform local training and collaboratively build robust models by sharing only weight updates, preserving data privacy while advancing model accuracy.

## Features

The `flower-serve` function includes the following features:

- **Scalability**: Supports a growing number of clients without performance degradation.
- **Data Privacy**: Ensures that only model updates are shared, keeping raw data secure.
- **Flexibility**: Compatible with various machine learning frameworks and models.
- **Monitoring Tools**: Provides insights into training progress and model performance.
- **Customizable Parameters**: Allows users to adjust training parameters for optimal results.


## Definition

```
flower_serve_function = project.new_function(
    name="flower-serve",
    kind="flower-server",
    requirements=["pandas==2.2.3", "flwr-datasets[vision]==0.5.0"]
)
```

## Usage

To utilize the `flower-serve` function, follow these steps:

1. **Initialize the Project**: Ensure that you have created the project and initialized the function as shown in the definition section.

2. **Build the Server**: Use the following code to build the server function.

    ```python
    flower_serve_func.run(action="build", wait=True)
    ```

3. **Deploy the Server**: Deploy the server using the following code.

    ```python
    run = flower_serve_func.run(action="deploy", insecure=True)
    ```

4. **Fetch the Service URL**: Retrieve the deployed service URL with the following code.

    ```python
    server_url = run.refresh().status.service['url'].split(':')[0] + ':9092' 
    print("Server URL:", server_url)
    ```

Notes: For detailed usage, check the usage notebook. 

## Client Usage

In order to use the server with clients, please refer to the [flower-client](https://scc-digitalhub.github.io/hub/functions/flower-client) function in the hub. This section provides detailed instructions on how to configure and connect client nodes.