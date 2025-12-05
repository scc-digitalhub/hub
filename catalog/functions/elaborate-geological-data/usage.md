# Elaboration

## 1. Fetch the `elaborate-geological-data` operation in the project

```python
function_rs = proj.get_function("elaborate-geological-data")
```

<p align="justify">The function represent a container runtime that allows you to deploy deployments, jobs and services on Kubernetes. It uses the base image of rs-flood-mapping container deploved in the context of project that creates the runtime environment required for the execution. It invovles pulling the base image with gdal installed and installing all the required libraries and launch instructions specified by 'launch.sh' file.</p>

## 2. Prepare data

Log the necessary artifacts (shape, map files) for the required area of interest before invoking 'elaborate-geological-data' operation. For e.g. shape file for Trentino regioncan be downloaded from the [WebGIS Portal](https://webgis.provincia.tn.it/) from https://siatservices.provincia.tn.it/idt/vector/p_TN_377793f1-1094-4e81-810e-403897418b23.zip. Unzip the files in a folder named 'Shapes_AOI' and then log it in project context.


```
artifact_name='Shapes_AOI'
src_path='/Shapes_AOI'
artifact_data = proj.log_artifact(name=artifact_name, kind="artifact", source=src_path)
```
Note that to invoke the operation on the platform, the data should be avaialble as an artifact on the platform datalake.

Log the Map aritfact with three files (slope map, aspect map, and legend.qml). For e.g trentino_slope_map.tiff, trentino_aspect_map.tiff, and legend.qml can be downloaded from the Huggingface repository. Copy the three files inside a folder 'Map' and log it as project artifact

```
artifact_name='Map'
src_path='Map'
artifact_data = proj.log_artifact(name=artifact_name, kind="artifact", source=src_path)
```

The resulting dataset will be registered as the project artifacts in the datalake under the name 'Shapes_AOI' and 'Map'.



## 3. Run

The function aims at downloading all the inputs from project context and perform the complex task of landslide monitoring analysis.

```python
run_el = function_elaborte.run(
    action="job",
    fs_group='8877',
    resources={
        "cpu": {"requests": "6", "limits": "12"},
        "mem": {"requests": "32Gi", "limits": "64Gi"}
    },
    volumes=[{
        "volume_type": "persistent_volume_claim",
        "name": "volume-land",
        "mount_path": "/app/files",
        "spec": { "size": "600Gi" }
    }],
    args=[
        '/shared/launch.sh',
        's1_ascending',
        's1_descending',
        '2020-11-01',
        '2020-11-14',
        'landslide_2020-11-01_2020-11-14',
        'Shapes_AOI',
        'ammprv_v.shp',
        'Map',
        'POLYGON ((10.595369 45.923394, 10.644894 45.923394, 10.644894 45.945838, \
                   10.595369 45.945838, 10.595369 45.923394))'
    ]
)            
```
