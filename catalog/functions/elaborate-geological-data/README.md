# Elaborate Geological Data

This function performs a complete preprocessing and analysis on geological Sentinel satellite data to extract information relevant to terrain composition, structural features, and surface variability. It detects and monitor ground deformation associated with landslides using Sentinel-1 Level-2A imagery. 
The function computes, for both ascending and descending directions, the interferometry between couples of images acquired every six days and derives the total displacement, coherence map, and local incident angle. It derives the horizontal and vertical displacement components from these products and merges them to obtain their cumulative sum and the displacement between each couple of images. The coherence maps are averaged, and the results are used to filter out the areas with the lowest coherence.

The function output GeoTiff Raster files containing:
- Cumulative sum and temporal variation of the horizontal displacement ;
- Cumulative sum and temporal variation of the vertical displacement;
- Cumulative sum and temporal variation of the total displacement of ascending and descending Sentinel-1 images;
- Cumulative sum of the horizontal displacement of the areas where the cumulative sum of the ascending and descending displacements has an opposite sign;
- Cumulative sum of the vertical displacement of the areas where the cumulative sum of the ascending and descending displacements has an opposite sign;
- Mean and temporal variation of the coherence maps;
- Mean and temporal variation of the coherence maps of ascending and descending Sentinel-1 images;
- Temporal variation of the C coefficient map representing the ratio of effective displacement computed in ascending and descending orbits;

The function is implemented as a container that allows you to deploy deployments, jobs and services on Kubernetes. It uses the base image with gdal, snapista, and scikit-learn libaries installed and confirgured. It further runs the launch instructions specified by 'launch.sh' file. 

## Definition
The function accepts a list of positional arguments that are passed directly to the Docker container. These parameters control Sentinel-1 data selection, temporal configuration, output aritifact, and AOI geometry. These arguments are passed to the container’s entrypoint script.


| Position | Value                                                                 | Description                                                                                                               |
|----------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| 1        | `/shared/launch.sh`                                                    | Entry-point script executed inside the Docker container. Handles download and preprocessing workflow.                    |
| 2        | `s1_ascending_landslide`                          | Name of artifact inside platform that contains Sentinel-1 ascending orbit cquisitions.                   |
| 3        | `s1_descending_landslide`                         | Name of artifact inside platform that contains Sentinel-1 descending orbit acquisitions.                                         |
| 4        | `2021-10-01`                                                            | Start date of monitoring period window.                                                                              |
| 5        | `2022-01-01`                                                            | End date of monitoring period window.                                                                                |
| 6        | `landslide_2021-10-01_2022-01-01`                                       | Name of output artifact.                                      |
| 7        | `Shapes_AOI`                                                             | Name of artifact inside platform containing regional shapefiles (e.g., Trentino region).                                                         |
| 8        | `ammprv_v.shp`                                                          | Name of specific shapefile inside to the artifact 'Shapes_AOI' used for spatial clipping/filtering.                                                                   |
| 9        | `Map`                                                                   | Name of artificat containing processing mode or output format label based on the workflow’s internal logic.                                           |
| 10       | `POLYGON ((10.595369 45.923394, 10.644894 45.923394, ...) )`           | WKT polygon defining the Area of Interest (AOI).                                                                          |

The function aims at downloading all the geological inputs specified in argument(s1_ascending_landslide, s1_descending_landslide, Shapes_AOI) from project context and perform the complex task of geological elaboration.

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
        "name": "volume-land",
        "mount_path": "/app/files",
        "spec": { "size": "600Gi" }
    }],
    args=[
        '/shared/launch.sh',
        's1_ascending',
        's1_descending',
        '2021-03-01',
        '2021-07-30',
        'landslide_2020-11-01_2020-11-14',
        'Shapes_AOI',
        'ammprv_v.shp',
        'Map',
        'POLYGON ((10.595369 45.923394, 10.644894 45.923394, 10.644894 45.945838, \
                   10.595369 45.945838, 10.595369 45.923394))'
    ]
)

```

## Usage

The function expect a entry point launch script as shown below giving user the possibility to configure the runtime environment prior to elaboration. It further runs the launch instructions specified by 'launch.sh' file. 

```
%%writefile "launch.sh"
#!/bin/bash
ls -la /shared
cd ~
pwd
source .bashrc
export PATH="/home/nonroot/miniforge3/snap/bin:$PATH"
export PROJ_LIB=/home/nonroot/miniforge3/share/proj
export GDAL_DATA=/home/nonroot/miniforge3/share/gdal
export GDAL_DRIVER_PATH=/home/nonroot/miniforge3/lib/gdalplugins
export PROJ_DATA=/home/nonroot/miniforge3/share/proj
cd /app
echo "{'s1_ascending': '$1', 's1_descending': '$2', 'startDate':'$3', 'endDate':'$4', 'outputArtifactName': '$5', 'shapeArtifactName': '$6', 'shapeFileName': '$7', 'mapArtifactName': '$8', 'geomWKT':'$9'}"
#export PATH="/home/nonroot/miniforge3/snap/.snap/auxdata/gdal/gdal-3-0-0/bin/:$PATH"
echo "GDAL DATA AFTER EXPORT:"
echo $GDAL_DATA
echo "PROJ_LIB AFTER EXPORT"
echo $PROJ_LIB
python main.py "{'s1_ascending': '$1', 's1_descending': '$2', 'startDate':'$3', 'endDate':'$4', 'outputArtifactName': '$5', 'shapeArtifactName': '$6', 'shapeFileName': '$7', 'mapArtifactName': '$8', 'geomWKT':'$9'}"
exit
```

```
function_elaborate = proj.new_function("elaborate",kind="container", image="ghcr.io/tn-aixpa/rs-landslide-monitoring:0.14.6", command="/bin/bash", code_src="launch.sh")
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
         "cpu": "12",
         "mem": "64Gi"
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
        '2021-03-01',
        '2021-07-30',
        'landslide_2020-11-01_2020-11-14',
        'Shapes_AOI',
        'ammprv_v.shp',
        'Map',
        'POLYGON ((10.595369 45.923394, 10.644894 45.923394, 10.644894 45.945838, \
                   10.595369 45.945838, 10.595369 45.923394))'
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
| `name`        | `volume-land`             | Volume identifier.                                          |
| `mount_path`  | `/app/files`              | Directory inside the container where the volume is mounted. |
| `size`        | `600Gi`                   | Allocated storage capacity.                                 |


'elaboration' consists of interferometry step which is a remote sensing technique that uses radar data to detect and monitor ground deformation associated with landslides and post processing steps which are computationally heavy since it is pixel based analysis. In some cases, the amount of sentinal data is huge that is why a default volume of 300Gi of type 'persistent_volume_claim' is specified in example to ensure significant data space. This configuration must be change according to scenario requirement. In the example given in documentation usage notebook, an elaboration on two weeks data is performed which takes ~5 hours to complete with 16 CPUs and 64GB Ram.
