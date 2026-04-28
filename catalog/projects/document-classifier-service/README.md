
# Document Classifier Service

This project implements a document classification service that trains and deploys a machine learning model to categorize text documents. It enables users to classify documents into predefined categories using a fine-tuned transformer model. The service is containerized and runs on Kubernetes, supporting both training and inference workflows.

## Features

The `document-classifier-service` function includes the following features:

- **Model training**: Fine-tune transformer-based models on custom document classification datasets
- **Configurable parameters**: Adjust learning rate, batch size, epochs, and other hyperparameters
- **GPU acceleration**: Optimized training with GPU support for faster model convergence
- **REST API inference**: Deploy trained models as REST endpoints for real-time predictions
- **Kubernetes-native**: Containerized deployment with automatic scaling and health monitoring
- **Model versioning**: Trained models are automatically logged and versioned on the platform
- **Persistent storage**: Support for persistent volumes to store training data and models
- **Custom environments**: Configure Hugging Face cache and other environment variables

## Definition

### document-classifier-train
A Python batch processing function that trains a document classification model.

**Key specifications:**

- Python version: 3.10
- Handler: Model training using transformer-based architectures
- Primary dependencies: Transformers, PyTorch, Hugging Face Hub
- Purpose: Fine-tunes a model on document classification tasks with configurable training parameters

### document-classifier-serve

A Python serving function that deploys the trained classification model as a REST API.

**Key specifications:**

- Python version: 3.10
- Handler: `src.serve:serve`
- Primary dependencies: Transformers, PyTorch, FastAPI
- Purpose: Serves the trained model for real-time document classification inference

## Usage

For a complete end-to-end example of training and deploying the document classifier, refer to the usage notebook. The notebook demonstrates:

1. **Project initialization** with the platform
2. **Training function setup** with custom hyperparameters
3. **Model training execution** with GPU resources
4. **Model versioning** and logging on the platform
5. **Serving function deployment** for inference
6. **Classification predictions** against the deployed service

The notebook provides step-by-step instructions and code examples for the complete training and serving workflow.

## Resources

These settings define the resource requests and limits for the runtime.

| Resource | Value | Description |
| -------- | ----- | ----------- |
| **GPU Type** | `A100` | GPU accelerator for model training and inference. |
| **Memory** | `6Gi` | Memory allocation for training and serving operations. |

The `document-classifier-service` function recommends GPU acceleration for efficient model training and inference.
