# Download Sentinel Data

## Definition

This function is used to download Sentinel satellite data efficiently. This function serves as the base for performing elaborations on different kinds of geospatial data processing tasks. Each elaboration comes with different sets of data requirements depending on the specific geospatial processing task and satellite data type being utilized. This function is configurable via a parameter object that controls the satellite data selection, temporal extent and spatial footprint. Key parameter groups:

- satelliteParams
    - satelliteType: Sentinel product family (e.g., "Sentinel-1", "Sentinel-2").
    - processingLevel: desired processing stage ("LEVEL1", "LEVEL2", ...).
    - sensorMode / polarization: sensor acquisition mode or polarization settings (mode names depend on satellite).
    - productType: product format (e.g., "SLC", "GRD", "L2A").
    - orbitDirection: pass "ASCENDING" or "DESCENDING".
    - relativeOrbitNumber: numeric orbit track identifier (optional).

- temporal and spatial
    - startDate / endDate: ISO date strings (YYYY-MM-DD) defining the search window.
    - geometry: spatial footprint in WKT or GeoJSON (polygon or bbox).
    - area_sampling: boolean toggle to enable area-level sampling.

- storage and runtime
    - tmp_path_same_folder_dwl: boolean to control temporary download placement.
    - artifact_name: name used for storing the downloaded artifact in the project context.

Notes and tips:
- Date ranges should be chosen to limit result sets; large ranges may require increased compute and storage.
- Use relativeOrbitNumber to filter by specific orbit tracks when needed.
- For Sentinel-2 searches you can also supply cloudCoverage thresholds; for Sentinel-1 specify polarization/product specifics.
- Ensure valid Copernicus credentials are available to the runtime via secrets before launching jobs.

Example parameter shape (illustrative):
{
    "satelliteParams": { "satelliteType": "Sentinel-1", "processingLevel": "LEVEL1", "productType": "SLC", "orbitDirection": "DESCENDING" },
    "startDate": "2021-01-01", "endDate": "2021-01-15",
    "geometry": "<WKT or GeoJSON>",
    "artifact_name": "download_output"
}

## Usage

The function is of kind container runtime that allows you to deploy deployments, jobs and services on Kubernetes. It uses the base image of sentinel-tools developed in the context of project which is a wrapper for the Sentinel download and preprocessing routine for the integration with the AIxPA platform. For more details [Click here](https://github.com/tn-aixpa/sentinel-tools/).

```python
string_dict_data = """{
     "satelliteParams":{
        "satelliteType": "Sentinel2",
        "bandmath": ["NDWI"]
     },
     "startDate": "2023-12-12",
     "endDate": "2019-12-30",
     "geometry": "POLYGON((10.88558452267069 46.2069331490752, 11.02591468396198 46.2069331490752, 11.02591468396198 46.288250617785245, 10.88558452267069 46.288250617785245, 10.88558452267069 46.2069331490752))",
     "cloudCover": "[0,5]",
     "area_sampling": "True",
     "artifact_name": "sentinel2_ndwi_area_sampling_2018"
 }"""


list_args =  ["main.py",string_dict_data]
function = proj.get_function("download-sentinel-data",kind="container",image="ghcr.io/tn-aixpa/sentinel-tools:latest",command="python")
```
Notes: For detailed usage see the usage notebook.

## Environment

The runtime environment of function consist of properties like
- CDSETOOL_ESA_PASSWORD
- CDSETOOL_ESA_USER

Register to the open data space copernicus(if not already) and get your credentials.

https://identity.dataspace.copernicus.eu/auth/realms/CDSE/login-actions/registration?client_id=cdse-public&tab_id=FIiRPJeoiX4

Log the credentials as project secret keys as shown below

```
# THIS NEED TO BE EXECUTED JUST ONCE
secret0 = proj.new_secret(name="CDSETOOL_ESA_USER", secret_value="esa_username")
secret1 = proj.new_secret(name="CDSETOOL_ESA_PASSWORD", secret_value="esa_password")
```

To avoid capacity issues the environment variable "TMPDIR" for this function execution is set to same path of volume mount. As a general confromance to best practice approach, the container runtime is executed as non root user(fs_group='8877')

```
function.run(
    action="job",
    secrets=["CDSETOOL_ESA_USER","CDSETOOL_ESA_PASSWORD"],
    fs_group='8877',
    args=["main.py", string_dict_data],
    envs=[{"name": "TMPDIR", "value": "/app/files"}],
    ...
    }])
```

## Resources

The resources for running this function varies as per the envisaged elaboration scenario requirements which depends on many factors such as type of elaboration, data period, index, geometry etc. The download-sentinel-data function depends on Sentinel Hub dataspace. It could happen that data download takes more time than usual due to various factors, including technical issues, data processing delays, and limitations in the data access infrastructure. Sentinel data has both temporal and spatial types, as it collects data over time (temporal) with specific spatial resolutions. The size of sentinal data payload in is normally large based on requirement of usecase scenario and requires a significant block of computing resources to executed which includes number of cpu, memory(Gi), and volume(Gi). The function performance improves with significant number of cpu and memory. In general, the recommended resources(cpu, memory) for running this function:

```json
{
    "resources": {
        "cpu": "6",
        "mem": "32Gi"
    }
}
```

Data volume requirements vary by scenario:
- **Single scene download**: 100–500 MB (Sentinel-1 GRD), 500–1000 MB (Sentinel-2 L2A)
- **Multi-temporal series**: Scales linearly with date range and area size
- **Large geographic areas**: May require 10+ GB for month-long searches
- **Band math / preprocessing**: Adds 20–30% overhead to storage needs

In order to run this function, a volume of type 'persistent_volume_claim' is specified to ensure significant data space. For example, the scenarios based on environmental degradation usecases like deorestation, vegetation loss are based on temporal analysis and requires downloading of big data over a period of time. On the other hand, the scenario based on natural disasters events requires downloading of different data payloads around a given event date, compute pre/post windows of data payloads for elaboration. Inside the usage notebook, one can find more fine grained resource configurations for different kinds of data analysis for e.g. one such example is the flood scenario for which the volume configuration for data payload (± 10 days) with respect to flood event date is shown below.

```json
{
    "volumes": [
        {
            "volume_type": "persistent_volume_claim",
            "name": "volume-flood",
            "mount_path": "/app/files",
            "spec": {
                "size": "100Gi"
            }
        }
    ]
}
```

For more detailed usage for different kind of scenario, check the usage notebook.

