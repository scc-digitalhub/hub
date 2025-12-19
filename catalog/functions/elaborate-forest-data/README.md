# Elaborate Deforestation Data

This function performs a complete preprocessing and analysis workflow for deforestation detection using Sentinel-2 Level-2A imagery. It operates on raw Sentinel-2 inputs provided in .SAFE or .zip format and focuses on the analysis of pre-downloaded spectral indices over a defined Area of Interest (AOI).

The workflow extracts vegetation and soil indicators, specifically the Normalized Difference Vegetation Index (NDVI) and the Bare Soil Index (BSI). These indices are interpolated to generate a monthly time series, enabling temporal consistency across acquisitions. Change detection is then performed using BFAST (Breaks For Additive Season and Trend) to identify structural breaks associated with deforestation events. The function produces change detection maps and deforestation probability maps as outputs.

Processing is carried out per Sentinel tile, allowing independent handling of overlapping tiles within the AOI (e.g. T32TQS, T32TPR, T32TPS, T32TQR). Each tile is processed separately to preserve spatial consistency and reduce edge effects. A Python-based clipping procedure is applied to convert the downloaded index data into AOI-specific input files. The clipped tiles are then used as inputs for the deforestation analysis pipeline.

This tile-based and AOI-focused approach ensures scalable, reproducible, and spatially accurate deforestation monitoring across heterogeneous regions.

The function provides complete workflow for
- Ingesting Sentinel-2 tile-specific temporal metadata.
- Perform elaboration
- Compute NDVI and BSI indices from RED, NIR, and SWIR1 bands.
- Apply cloud/shadow masks from precomputed binary mask files (MASK.npy).
- Interpolate data to generate a complete 24-month time series (12 months/year).
- Fuse features and reshape data into pixel-wise time series.
- Run BFAST to detect change points across time.
- Post-process change maps to remove isolated pixels and fill gaps.
- Log results as GeoTIFF raster files.

The function is implemented as a container that allows you to deploy deployments, jobs and services on Kubernetes. It uses the base image with gdal, snapista, and scikit-learn libaries installed and pre configured. It further runs the launch instructions specified by 'launch.sh' file. 

## Definition
The function accepts a list of positional arguments that are passed directly to the Docker container. These parameters include pre-downloaded Sentinel-2 indices for a specified Area of Interest (AOI) and temporal range, producing deforestation change and probability outputs. These arguments are passed to the container’s entrypoint script.

| Position | Argument                    | Description                                                               |
| -------- | --------------------------- | ------------------------------------------------------------------------- |
| 1        | `/shared/launch.sh`         | Bash entrypoint script executed when the container starts.                |
| 2        | `Shapes_AOI`                | Loggged Artifact name for AOI shapefile used for spatial clipping.        |
| 3        | `data_s2_2018_19_tps`       | Logged artifact name for Sentinel-2 dataset (indices already downloaded). |
| 4        | `[2018,2019]`               | Temporal range (years) used to build the NDVI/BSI time series.            |
| 5        | `deforestation_2018_19_tps` | Output name / scenario identifier for generated results.                  |


The function aims at downloading all the inputs specified in argument(data_s2_2018_19_tps, Shapes_AOI) from project context and perform the complex task of deforestation elaboration.

Example

The following command launches the elaborate function as a containerized job, providing compute resources, storage volumes, and runtime arguments.

```
run_el = function_rs.run(
    action="job",
    fs_group='8877',
    resources={
         "cpu": "12",
         "mem": "64Gi"
    },
    volumes=[{
        "volume_type": "persistent_volume_claim",
        "name": "volume-deforestation",
        "mount_path": "/app/files",
        "spec": { "size": "250Gi" }
    }],
    args=[
        '/shared/launch.sh',
        'Shapes_AOI',
        'data_s2_2018_19_tps',
        "[2018,2019]",
        'deforestation_2018_19_tps'
    ]
)

```

## Usage

The function expect a entry point launch script as shown below giving user the possibility to configure the runtime environment prior to elaboration. It further runs the launch instructions specified by 'launch.sh' file. 

```
#!/bin/bash
ls -la /shared
cd ~
pwd
source .bashrc
echo "GDAL version:"
gdal-config --version
python --version
echo "GDAL DATA:"
echo $GDAL_DATA
echo "PROJ_LIB"
echo $PROJ_LIB
cd /app
echo "{'shapeArtifactName': '$1', 'dataArtifactName': '$2', 'years':$3, 'outputArtifactName': '$4'}"
export PROJ_LIB=/home/nonroot/miniforge3/share/proj
export GDAL_DATA=/home/nonroot/miniforge3/share/gdal
#export PATH="/home/nonroot/miniforge3/snap/.snap/auxdata/gdal/gdal-3-0-0/bin/:$PATH"
echo "GDAL DATA AFTER EXPORT:"
echo $GDAL_DATA
echo "PROJ_LIB AFTER EXPORT"
echo $PROJ_LIB
python main.py "{'shapeArtifactName': '$1', 'dataArtifactName': '$2', 'years':$3, 'outputArtifactName': '$4'}"
exit
```

```
function_elaborate = proj.new_function("elaborate",kind="container", image="ghcr.io/tn-aixpa/rs-deforestation:0.14.6", command="/bin/bash", code_src="launch.sh")
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
function_elaborate.un(
    action="job",
    fs_group='8877',
    resources={
         "cpu": "12",
         "mem": "64Gi"
    },
    volumes=[{
        "volume_type": "persistent_volume_claim",
        "name": "volume-deforestation",
        "mount_path": "/app/files",
        "spec": { "size": "250Gi" }
    }],
    args=[
        '/shared/launch.sh',
        'Shapes_AOI',
        'data_s2_2018_19_tps',
        "[2018,2019]",
        'deforestation_2018_19_tps'
    ]
)
```
To avoid capacity issues the environment variable "TMPDIR" for this function execution is set to same path of volume mount. As a general confromance to best practice approach, the container runtime is executed as non root user(fs_group='8877')


## Resources

These settings define the resource requests and limits for the container runtime.

| Resource   | Requests| Description                                            |
| ---------- | --------| ------------------------------------------------------ |
| **CPU**    | `12`    | CPU cores allocated to the job.    |
| **Memory** | `64Gi`  | Memory available to the container. |

The job mounts a persistent storage volume used for reading/writing large datasets (e.g., Sentinel images).

| Field         | Value                     | Description                                                 |
| ------------- | ------------------------- | ----------------------------------------------------------- |
| `volume_type` | `persistent_volume_claim` | Indicates a persistent storage resource.                    |
| `name`        | `volume-deforestation`    | Volume identifier.                                          |
| `mount_path`  | `/app/files`              | Directory inside the container where the volume is mounted. |
| `size`        | `250Gi`                   | Allocated storage capacity.                                 |


'elaboration' consists of interpolation and post processing steps which are computationally heavy since it is pixel based analysis. It is based on python joblib library for optimizations of numpy arrays. With the use of more images the interpolation will be shorter. The amount of sentinal data is huge that is why a volume of 250Gi of type 'persistent_volume_claim' is specified to ensure significant data space. On average the TPS tiles takes around 8-10 hours to complete with 16 CPUs and 64GB Ram for 2 years of data which is the default period.