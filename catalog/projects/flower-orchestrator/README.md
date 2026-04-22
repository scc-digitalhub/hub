# Flower Orchestrator

This project implements a federated learning orchestration service using Flower (Floral). It coordinates distributed machine learning training across multiple clients and a central server, enabling collaborative model training while preserving data privacy. The service is containerized and runs on Kubernetes, supporting secure and insecure federation modes.

## Features

The `flower-orchestrator` project includes the following features:

- **Federated learning coordination**: Orchestrate distributed training across multiple client nodes
- **Flower Server deployment**: Central aggregation server for model updates
- **Flower Client nodes**: Multiple participating clients for federated training
- **Flower App execution**: Coordinate training rounds and model convergence
- **Configurable parameters**: Adjust partition strategy, local epochs, and training rounds
- **GPU acceleration**: Optimized training with GPU support across distributed nodes
- **Security modes**: Support for both secure (TLS) and insecure modes
- **Node authentication**: Optional public-private key-based node authentication
- **Model versioning**: Trained models are automatically logged and versioned on the platform
- **REST API monitoring**: Real-time access to server and client status

## Definition

### flower-serve

A Flower server function that acts as the central aggregator for federated learning.

**Key specifications:**

- Kind: `flower-server`
- Primary dependencies: Pandas, Floral Datasets
- Purpose: Aggregates model updates from multiple clients

### flower-client

A Flower client function that participates in federated training.

**Key specifications:**

- Kind: `flower-client`
- Primary dependencies: Pandas, Floral Datasets
- Purpose: Trains local models and sends updates to the server

### flower-app

A Flower application function that orchestrates the federated learning execution.

**Key specifications:**

- Purpose: Coordinates training rounds and manages the federation lifecycle

## Usage

For a complete end-to-end example of setting up and running federated learning, refer to the usage notebook. The notebook demonstrates:

1. **Project initialization** with digital hub
2. **Server deployment** with insecure mode configuration
3. **Client deployment** with partition strategies
4. **Federation execution** with configurable hyperparameters
5. **Status monitoring** through service URLs and logs

## Resources

These settings define the resource requests and limits for the runtime.

| Resource | Value | Description |
| -------- | ----- | ----------- |
| **Port** | `9092` | Service port for Flower superlink communication |
| **API Port** | `9093` | Execution API port for application coordination |
