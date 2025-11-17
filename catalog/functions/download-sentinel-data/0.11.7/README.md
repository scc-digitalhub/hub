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

The function is of kind container runtime that allows you to deploy deployments, jobs and services on Kubernetes. It uses the base image of sentinel-tools deploved in the context of project which is a wrapper for the Sentinel download and preprocessing routine for the integration with the AIxPA platform. For more details [Click here](https://github.com/tn-aixpa/sentinel-tools/).

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
function = proj.get_function("download-sentinel-data",kind="container",image="ghcr.io/tn-aixpa/sentinel-tools:0.11.7",command="python")
```
Notes: For detailed usage see the usage notebook (usage.ipynb)

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

## Resources

Recommended resources(cpu, memory) for running this function:

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

Plan temporary storage (`tmp_path_same_folder_dwl`) accordingly to avoid capacity issues.

Recommend volume for running this function in flood analysis scenario is.


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

For more detailed usage for different kind of scenario, check the <a href='usage.ipynb'>usage notebook</a>.

