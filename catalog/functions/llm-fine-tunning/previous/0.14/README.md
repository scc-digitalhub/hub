
# LLM Fine-Tuning Function

## Overview

This function provides a template for fine-tuning large language models (LLMs) using the Hugging Face Transformers library. It enables structured training and logging of LLMs, allowing you to customize the training process with your own datasets and configurations.

## Prerequisites

1. **Hugging Face Token**: Create a token at [Hugging Face Settings → Access Tokens](https://huggingface.co/settings/tokens)
2. **Store as Secret**: Save the token as a project secret named `HF_TOKEN`
3. **GPU Resource**: Ensure sufficient GPU resources (e.g., 1xV100) are available

## Quick Start

### 1. Initialize Project

```python
import digitalhub as dh

PROJECT_NAME = "<YOUR_PROJECT_NAME>"
proj = dh.get_or_create_project(PROJECT_NAME)
```

### 2. Deploy Training Function

```python
function_train = proj.get_function("train-llm")
func_b = function_train.run(action='build', wait=True)
```

### 3. Run Training Job

```python
train_run = function_train.run(
    action="job",
    profile="1xV100",
    parameters={
        "model_id": "meta-llama/Llama-3.1-8B",
        "model_name": "llmpa-tracked",
        "hf_dataset_name": "team-bay/data-science-qa",
        "train_data_path": "DataScienceDataset.csv",
        "dev_data_path": "DataScienceDataset.csv",
        "num_epochs": 2
    },
    secrets=["HF_TOKEN"],
    volumes=[{
        "volume_type": "persistent_volume_claim",
        "name": "volume-llmpa",
        "mount_path": "/app/local_data",
        "spec": {"size": "50Gi"}
    }]
)
```

## Key Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_id` | str | - | Hugging Face model identifier |
| `num_epochs` | int | 10 | Number of training epochs |
| `learning_rate` | float | 5e-5 | Learning rate for optimization |
| `lora_rank` | int | 16 | LoRA rank for adapter training |
| `quantization` | int | 4 | 0=none, 4=4-bit quantization |
| `train_batch_size` | int | 3 | Training batch size |
| `eval_batch_size` | int | 2 | Evaluation batch size |

## Features

- **LoRA Adaptation**: Efficient fine-tuning with Low-Rank Adapters
- **Quantization Support**: 4-bit quantization for memory efficiency
- **Early Stopping**: Prevents overfitting with configurable patience
- **Logging Integration**: Weights & Biases (wandb) support for experiment tracking
- **GPU Optimized**: Automatic CUDA acceleration

For more detailed usage see the notebook.
