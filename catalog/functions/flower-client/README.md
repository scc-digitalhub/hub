# Flower Client

The `flower-client` function is a federated learning client that connects to a Flower server to participate in collaborative model training. It enables distributed machine learning by allowing multiple clients to train models locally on their data partitions while only sharing model updates with the server, ensuring data privacy and reducing communication overhead. 

It is essential to set up the `flower-serve` function before deploying the client. The server acts as the central coordinator for the federated learning process, managing the communication between clients and ensuring that model updates are aggregated correctly. Proper configuration of the server is crucial for the successful operation of the client nodes, as they rely on the server to facilitate training and data privacy. Make sure to follow the setup instructions carefully to ensure a smooth deployment of the client following the hub function [flower-serve](https://scc-digitalhub.github.io/hub/functions/flower-serve) function in the hub. This section provides detailed instructions on how to configure and deploy flower server node.

## Features

The `flower-client` function includes the following features:

- **Scalability**: Supports a growing number of clients without performance degradation.
- **Data Privacy**: Ensures that only model updates are shared, keeping raw data secure.
- **Flexibility**: Compatible with various machine learning frameworks and models.
- **Customizable Parameters**: Allows users to adjust training parameters for optimal results.


## Definition

```
flower_client_function = project.new_function(
    name="flower-client",
    kind="flower-client",
    requirements=["pandas==2.2.3", "flwr-datasets[vision]==0.5.0"]
)
```

## Usage

To utilize the `flower-client` function, follow these steps:

1. **Initialize the Project**: Ensure that you have created the project and initialized the function as shown in the definition section.

2. **Build the Client**: Use the following code to build the server function.

    ```python
    flower_client_func.run(action="build", wait=True)
    ```

3. **Deploy the Client**: Deploy the client after server is up and running. Fetch the server url and start the client using the following code.

    ```python
    server_url = server_run.refresh().status.service['url'].split(':')[0] + ':9092' 
    
    # Deploy client 1
    run = client_function.run(action="deploy", superlink=server_url, node_config={
            "partition-id": 0,
            "num-partitions": 3,
            "local-epochs": 2
            })

    # Deploy client 2
    run = client_function.run(action="deploy", superlink=server_url, node_config={
            "partition-id": 1,
            "num-partitions": 3,
            "local-epochs": 2
             })

    # Deploy client 3
    run = client_function.run(action="deploy", superlink=server_url, node_config={
            "partition-id": 2,
            "num-partitions": 3,
            "local-epochs": 2
            })
    ```


Notes: For detailed usage, check the usage notebook. 

In order to use the perform federated training using flower server with clients, please refer to the [flower-job](https://scc-digitalhub.github.io/hub/functions/flower-job) function in the hub. This section provides detailed instructions on how to configure and connect client nodes with server to perform federatd training.