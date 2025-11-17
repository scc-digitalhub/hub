# How to document catalog entries

The catalog aims at supporting the following types of entities

- functions: represent executable operations on the platform
- dataitems: tabular datasets
- artifacts: datasets with arbitrary structure
- models: ML/AI model artifacts
- products: complete AI-based solution integrating a set of single elements in a coherent manner

Each entry in the catalog should be documented under the corresponding catalog subsection. Specifically, for each entry
it is necessary to create a folder that contains the following obligatory entries:

- `.yaml` file with the structured specification of the entity
- `README.md` file with the description of the entry, usage, and properties (see corresponding subsection for details).
- `notebook.ipynb`  notebook file with the instructions on how to use it directly in the platform.

Besides, it is possible to provide additional information and files. Do not put the complete artifacts (e.g., models, datasets, etc) here; rather use the corresponding repositories for this purpose (e.g., Github, Huggingface, etc).

## Versioning

Each entry may contain one or more version of the specification. The latest available version should be made available in the root folder of the entry. Each other version should be placed in a subfolder with the corresponding version in the name of the folder.

## General Classification

In order to support the classification, search, and navigation within the catalog, each entry should be provided with a set of classification labels. These labels should have predefined prefixes to facilitate their indexing. More specifically, it is necessary to provide the information about

- `license:<spdx-identifier>`: license information defined with the corresponding SPDX identifier or 'other' if identififer is not present.
- `domain:<data-domain>`: data domain tag defining the type of the data managed by the entity. May refer to
  - `nlp` for text
  - `audio` for audio
  - `vision` for images and videos
  - `tabular` for tabular data
  - `geo` for geographical data formats
  - `multimodal` for mixture of data types
  - `other` for all other cases
- `application:<application-domain>`: to describe application domains. It is possible to use many values for the same entry. Examples include, but not limited to
  - `pa` for public administration services
  - `agriculture` 
  - `healthcare`
  - `industry`
- `aspect:<aspect>`: to describe specific dimensions of the entity usage/application. May be omitted if the entity does not address any specific aspect. Examples include, but not limited to
  - `quality` for quality control
  - `security` for security
  - `privacy` for privacy
  - `accessibility` for accessibility
  - `fairness` for fairness and legal compliance
  - `performance` for performance
- `platform:<platform>`: minimal platform version tag supporting the entity. 
 
  
 Each entity type defines its own set of predefined labels.

 Besides, it is possible to define arbitrary custom tags.

## 1. Function Documentation

### Function classification
To document a function, it is necessary to provide additional set of tags:

- `type:<type>` type of the function being `job` or `service`.
- `phase:<phase>` phase of the life-cycle of the application to which the function is associated. This includes
  - `data-preparation`: operation refers to data preprocessing and analysis phase
  - `data-validation`: operation refers to data quality analysis
  - `feature-extraction`: operation refers to feature extraction phase
  - `model-training`: operation refers to model training phase
  - `model-evaluation`: operation refers to model evaluation (testing, validation) phase
  - `model-serving`: operation refers to model serving phase considering the execution and interaction
  - `monitoring`: operation refers to model/application monitoring 
  - `reporting`: operation refers to model reporting and documentation 
  - `utility`: operation refers to utility functions not directly related to any of the above phases
- `framework:<framework>` framework in which the function is implemented. It is possible to use many values for the same entry. Examples include, but not limited to
  - `pytorch`
  - `tensorflow`
  - `huggingface`
  - `sklearn`
- `inference:<inference-framework>` inference model that the function targets (if applicable). This may include
  - `openai` for OpenAI-compatible models and services
  - `oi` for OpenInference-compatible models and services
  - `custom` for custom models and services

### Function specification

The function specification file should contain the full spec as of platform as well as the function run template to be used for function execution.

### Function description

The README file of the function specification should contain the following sections:

- `Description`: textual description of the function.
- `Definition`: detailed description of the function signature, inputs, and outputs. Depending on runtime this amounts to defining the function parameters or arguments, produced artifacts or output data, etc.
- `Usage`: instructions on how to use the function in the platform (may be reference to the corresponding notebook sections).
- `Environment`: description of the runtime environment properties and secrets required by the function execution.
- `Resources`: description of the runtime resources required by the function execution including memory, cpu, GPU, and data volume properties to consider.

# Function usage notebook

The function usage notebook is a Jupyter notebook file that provides instructions on how to use the function in the platform. It should contain the following steps:

- creating a project and corresponding environment (e.g., secrets if necessary).
- registering the function in the platform.
- creating / registering necessary artifacts to use the function (e.g., data it will consume).
- instructions to build the function if necessary.
- different examples of function execution with different corresponding configurations.
- demonstration of the function outcomes. If the function is a job, showcase the output artifacts. If the function is a service, show the service invocation example and relevant outputs.