# Elaborate Flood Data

This function performs flood analysis using Sentinel satellite data to assess flood extent and impact. It processes raw .SAFE or .zip Sentinel inputs, computes water indices, predicts water before and after a flood event, and outputs flood detection layer.

The function provides complete workflow for
- Ingesting Sentinel-1 (scene-based) and Sentinel-2 (tile-based) data using product-specific metadata.
- Perform elaboration
- Compute NDWI indices from Sentinel-2 imagery to detect water bodies before and after the flood event.z
- Calculate flood extent by analyzing pre- and post-event backscatter differences from Sentinel-1 data
- Combine both results from Sentinel-1 and Sentinel-2 to have one flood prediction layer.
- Post-process change maps to improve the results by masking permanent water bodies.
- Log results as GeoTIFF raster files Raster and vector outputs.

The function is implemented as a container that allows you to deploy deployments, jobs and services on Kubernetes. It uses the base image with gdal, snapista, and scikit-learn libaries installed and confirgured. It further runs the launch instructions specified by 'launch.sh' file. 

## Definition
The function accepts a list of positional arguments that are passed directly to the Docker container. These parameters control Sentinel data selection, temporal configuration, output aritifact, and AOI geometry. These arguments are passed to the container’s entrypoint script.

These arguments define inputs, geospatial filters, auxiliary data, processing parameters, and scenario metadata.

| Pos | Value                     | Description                                                         |
| --- | ------------------------- | ------------------------------------------------------------------- |
| 1   | `/shared/launch.sh`       | Entrypoint script executed in the container.                        |
| 2   | `sentinel1_GRD_preflood`  | Sentinel-1 GRD dataset for the pre-flood period.                    |
| 3   | `sentinel1_GRD_postflood` | Sentinel-1 GRD dataset for the post-flood period.                   |
| 4   | `sentinel2_pre_flood`     | Sentinel-2 optical dataset for the pre-flood period.                |
| 5   | `sentinel2_post_flood`    | Sentinel-2 optical dataset for the post-flood period.               |
| 6   | `POLYGON ((...))`         | WKT geometry defining AOI for flood analysis.                       |
| 7   | `Slopes_TN`               | Artifact of slope map resources.                                    |
| 8   | `trentino_slope_map.tif`  | Name of Slope raster file inside 'Slopes_TN' artifact.              |
| 9   | `Lakes_TN`                | Artifact for lake datasets.                                         |
| 10  | `idrspacq.shp`            | Name of specific Lake shapefile inside 'Lakes_TN' artifact          |
| 11  | `Rivers_TN`               | Artifact for river datasets.                                        |
| 12  | `cif_pta2022_v.shp`       | Name of River network shapefile inside 'Rivers_TN' artifact.        |
| 13  | `garda_oct_2020`          | output name                                                         |
| 14  | `2020-10-02`              | Event date of flood.                               |
| 15  | `EPSG:25832`              | Spatial reference system for output products.                       |
| 16  | `['VV','VH']`             | Sentinel-1 polarizations to process.                                |
| 17  | `700`                     | Processing threshold (e.g., buffer, intensity, or scale parameter). |
| 18  | `7`                       | Filter/window size parameter.                                       |
| 19  | `15`                      | Processing radius or kernel size.                                   |
| 20  | `2`                       | Flood-level classification/threshold parameter.                     |
| 21  | `val di fassa`            | Region name used for contextual labeling.                           |


Example

The following command launches the elaborate function as a containerized job, providing compute resources, storage volumes, and runtime arguments.

```
run_el = function_rs.run(
    action="job",
    fs_group='8877',
    resources={
         "cpu": "6",
         "mem": "64Gi"
    },
    volumes=[{
        "volume_type": "persistent_volume_claim",
        "name": "volume-flood",
        "mount_path": "/app/data",
        "spec": { "size": "100Gi" }
    }],
    args=[
        '/shared/launch.sh',
        'sentinel1_GRD_preflood',
        'sentinel1_GRD_postflood',
        'sentinel2_pre_flood',
        'sentinel2_post_flood',
        'POLYGON ((10.644988646837982 45.85539621678084, 10.644988646837982 46.06780100571985, 10.991744628283294 46.06780100571985, 10.991744628283294 45.85539621678084, 10.644988646837982 45.85539621678084))',
        'Slopes_TN',
        'trentino_slope_map.tif',
        'Lakes_TN',
        'idrspacq.shp',
        'Rivers_TN',
        'cif_pta2022_v.shp',
        'garda_oct_2020',
        '2020-10-02',
        'EPSG:25832',
        "['VV','VH']",
        '700',
        '7',
        '15',
        '2',
        'val di fassa'
        ]
    )
```

## Usage

The function expect a entry point launch script as shown below giving user the possibility to configure the runtime environment prior to elaboration. It further runs the launch instructions specified by 'launch.sh' file. 

```
%#!/bin/bash
ls -la /shared
cd ~
pwd
source .bashrc
export PATH="/home/nonroot/miniforge3/snap/bin:$PATH"
export PROJ_LIB=/home/nonroot/miniforge3/share/proj
export GDAL_DATA=/home/nonroot/miniforge3/share/gdal
export GDAL_DRIVER_PATH=/home/nonroot/miniforge3/lib/gdalplugins
export PROJ_DATA=/home/nonroot/miniforge3/share/proj
gdal-config --version
python --version
echo "GDAL DATA AFTER EXPORT:"
echo $GDAL_DATA
echo "PROJ_LIB AFTER EXPORT"
echo $PROJ_LIB
echo "Running flood mapping script with parameters:"
echo "{'s1PreFlood': '$1', 's1PostFlood':'$2', 's2PreFlood':'$3','s2PostFlood':'$4','geomWKT':'$5','slopeArtifact':'$6','slopeFileName':'$7','lakeShapeArtifactName':'$8','lakeShapeFileName':'$9','riverShapeArtifactName':'${10}','riverShapeFileName':'${11}','output':'${12}','eventDate':'${13}','targetCRS':'${14}','polarization':${15},'dem_threshold':${16},'slope_threshold':${17},'noise_min_pixels':${18},'river_buffer_meters':${19}}, 'aoi_name':'${20}'}"
cd /app
python main.py "{'s1PreFlood':'$1', 's1PostFlood':'$2', 's2PreFlood':'$3','s2PostFlood':'$4','geomWKT':'$5','slopeArtifact':'$6','slopeFileName':'$7','lakeShapeArtifactName':'$8','lakeShapeFileName':'$9','riverShapeArtifactName':'${10}','riverShapeFileName':'${11}','output':'${12}','eventDate':'${13}','targetCRS':'${14}','polarization':${15},'dem_threshold':${16},'slope_threshold':${17},'noise_min_pixels':${18},'river_buffer_meters':${19}, 'aoi_name':'${20}'}"
exit
```

```
function_elaborate = proj.new_function("elaborate",kind="container", image="ghcr.io/tn-aixpa/rs-flood-mapping:0.14.6", command="/bin/bash", code_src="launch.sh")
```
Notes: For detailed usage see the usage notebook.


## Environment

The runtime environment of function consist of properties which are configured in the bash script created in previous section
- PATH
- PROJ_LIB
- GDAL_DATA
- GDAL_DRIVER_PATH
- PROJ_DATA


```
function_elaborate.run(
    action="job",
    fs_group='8877',
    resources={
         "cpu": "6",
         "mem": "64Gi"
    },
    volumes=[{
        "volume_type": "persistent_volume_claim",
        "name": "volume-flood",
        "mount_path": "/app/data",
        "spec": { "size": "100Gi" }
    }],
    args=[
        '/shared/launch.sh',
        'sentinel1_GRD_preflood',
        'sentinel1_GRD_postflood',
        'sentinel2_pre_flood',
        'sentinel2_post_flood',
        'POLYGON ((10.644988646837982 45.85539621678084, 10.644988646837982 46.06780100571985, 10.991744628283294 46.06780100571985, 10.991744628283294 45.85539621678084, 10.644988646837982 45.85539621678084))',
        'Slopes_TN',
        'trentino_slope_map.tif',
        'Lakes_TN',
        'idrspacq.shp',
        'Rivers_TN',
        'cif_pta2022_v.shp',
        'garda_oct_2020',
        '2020-10-02',
        'EPSG:25832',
        "['VV','VH']",
        '700',
        '7',
        '15',
        '2',
        'val di fassa'
        ]
    )
```
To avoid capacity issues the environment variable "TMPDIR" for this function execution is set to same path of volume mount. As a general confromance to best practice approach, the container runtime is executed as non root user(fs_group='8877')


## Resources

These settings define the resource requests and limits for the container runtime.

| Resource   | Requests | Description                                            |
| ---------- | -------- | ------------------------------------------------------ |
| **CPU**    | `6`      | CPU cores allocated to the job.    |
| **Memory** | `64Gi`   | Memory available to the container. |

The job mounts a persistent storage volume used for reading/writing large datasets (e.g., Sentinel images).

| Field         | Value                     | Description                                                 |
| ------------- | ------------------------- | ----------------------------------------------------------- |
| `volume_type` | `persistent_volume_claim` | Indicates a persistent storage resource.                    |
| `name`        | `volume-flood`            | Volume identifier.                                          |
| `mount_path`  | `/app/files`              | Directory inside the container where the volume is mounted. |
| `size`        | `100Gi`                   | Allocated storage capacity.                                 |


'elaboration' function consists of interpolation and post processing steps which are computationally heavy since it is pixel based analysis. The amount of sentinal data is huge that is whay a volume of 100Gi of type 'persistent_volume_claim' is specified to ensure significant data spacetake several hours to complete with 16 CPUs and 64GB Ram for processing data window around flood event date (±20 days sentinel-2 data and ± 7days Sentinel-1 data)which is the default period.
