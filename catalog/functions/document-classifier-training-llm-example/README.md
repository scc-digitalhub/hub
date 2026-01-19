# Document Classifier Training with LLM

This function provides a machine learning function for training a document classification model using BERT (Bidirectional Encoder Representations from Transformers). The classifier can categorize documents into multiple classes based on their text content.

## Overview

The function implements a multiclass sequence classifier fine-tuned on Italian text, designed to automatically assign taxonomy labels to documents based on their title, description, and objective.

## Features

This function demonstrates a minimal example of a multiclass sequence classifier based on BERT base Italian, fine-tuned on a test dataset. The classifier is trained to suggest one or more labels from the taxonomy needed to categorize documents. When given a title, a description, and an objective, the classifier can predict the appropriate label from the taxonomy in use. The model can be further fine-tuned on new data.

It demonstrate how to train classification model with BERT (Bidirectional Encoder Representations from Transformers). The classifier model is trained to suggest one or more labels within the input data. The training data looks like following table


| |text| labels |
|-|----|--------|
|0|text1....| 11
|1|text2....| 12

You can use the provided [sample train dataset](/src/train_data.csv). It is also used in the embedded script as training and validation dataset. Ensure that your dataset includes a `text` column containing the document content and a `labels` column with the corresponding category labels. The dataset should be balanced, meaning each label should have a similar number of examples to avoid bias during training.


## Definition

The function is defined with the following key components:

- **Handler**: train (The entry point method that processes training requests)
- **Embedded**: The training logic is embedded directly in the function definition, including data preprocessing, model training, and evaluation steps
- **Parameters**: 
 **target_model_name**: Name of the model to save
    - **num_train_epochs**: Number of training epochs
    - **per_device_train_batch_size**: Batch size for training
    - **per_device_eval_batch_size**: Batch size for evaluation
    - **gradient_accumulation_steps**: Number of steps to accumulate gradients
    - **weight_decay**: Weight decay for regularization
    - **learning_rate**: Learning rate for optimization
    - **lr_scheduler_type**: Type of learning rate scheduler

    
- **Outputs**: 
    - Trained BERT-based classification model
    - Training metrics and evaluation results




